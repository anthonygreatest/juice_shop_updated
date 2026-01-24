from data.generators.generator import CardGenerator
from utils.schemas.add_credit_card_request import AddCreditCardRequest


class CreditCardModule:

    def create_credit_card_request(self, data, schema):

        data = {key: value for key, value in data.__dict__.items()}

        return schema(**data)
