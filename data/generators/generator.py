import random

from faker import Faker
from data.dataclasses.container import Password, CreditCard, ProfileName

class BaseFakerGenerator:

    def __init__(self):
        self.faker = Faker()

class PassGenerator(BaseFakerGenerator):

    def create_random_pass(self):

        return Password(
            password=self.faker.password()
        )

class CardGenerator(BaseFakerGenerator):

    def create_credit_card(self):

        cards = ['visa', 'mastercard']

        return CreditCard(
            full_name=self.faker.name().upper(),
            card_num=self.faker.credit_card_number(card_type=random.choice(cards)),
            exp_year=str(random.randint(2080, 2099)),
            exp_month=str(random.randint(1, 12)),
        )

class NameGenerator(BaseFakerGenerator):

    def create_name(self):

        return ProfileName(
            username=self.faker.name()
        )

class GenerateLongEmail(BaseFakerGenerator):

    def generate_long_email(self):

        email_text = (self.faker.text(max_nb_chars=200).replace(' ', '').replace('.', '_').replace('\n', '').rstrip('_')).lower()

        return f'{email_text}@{self.faker.domain_name()}'

# class RawCardGenerator(BaseFakerGenerator):
#
#     def create_credit_card(self):
#
#         cards = ['visa', 'mastercard']
#
#         return {'fullName': self.faker.name().upper(),
#                 'cardNum': self.faker.credit_card_number(card_type=random.choice(cards)),
#                 'expYear': str(random.randint(2080, 2099)),
#                 'expMonth': str(random.randint(1, 12))}
