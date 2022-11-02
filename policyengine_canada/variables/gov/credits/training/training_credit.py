from math import remainder
from policyengine_canada.model_api import *


class training_credit(Variable):
    value_type = float
    entity = Person
    label = "Training credit"
    unit = CAD
    documentation = "Training credit available"
    definition_period = YEAR

    def formula(tax_unit, period, parameters):
        income = tax_unit("employment_income", period)
        # TODO: ^ the above income concept should include maternity & parental benefits + working income (employment + self-employment income)
        tuition = tax_unit("tuition_expenses", period)
        age = tax_unit("age", period)
        training = parameters(period).gov.credits.training
        lower_limit = training.age_bracket_lower
        upper_limit = training.age_bracket_upper
        aged = (age >= lower_limit) & (age <= upper_limit)
        existing_credits = tax_unit("existing_training_credits", period)
        cap = training.total_cap
        remaining = max_(0, cap - existing_credits)
        threshold = training.income_threshold
        credits = threshold.calc(income)
        # TODO: test for age and tuition paid
        return min_(remaining, credits)
