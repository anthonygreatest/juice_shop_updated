from data.builder import BuilderOrder, BuilderCheckout, BuilderFeedback, BuilderRecycle, \
    BuilderPassReset, UserBuilder, BuilderAddress, DigitalWalletBuilder, ReviewBuilder
from data.generators.generator import CardGenerator, NameGenerator, PassGenerator
from data.generators.pass_generator import PasswordPairGenerator
from data.generators.recycle_date_generator import DateGenerator
from data.generators.review_generator import ReviewGenerator, FeedbackGenerator


class DataFactory:

    generators = {
        'random_password': PassGenerator,
        'credit_card': CardGenerator,
        'password_pair': PasswordPairGenerator,
        'name': NameGenerator,
        'date_generator': DateGenerator,
        'review_generator': ReviewGenerator,
        'feedback_generator': FeedbackGenerator
    }

    builders = {
        'register': UserBuilder,
        'new_pass': BuilderPassReset,
        'order': BuilderOrder,
        'delivery_address': BuilderAddress,
        'checkout': BuilderCheckout,
        'feedback': BuilderFeedback,
        'recycle': BuilderRecycle,
        'digital_wallet': DigitalWalletBuilder,
        'review': ReviewBuilder
    }

    @classmethod
    def get_builder(cls, name, *args, **kwargs):
        if name not in cls.builders:
            raise ValueError(f'Unknown builder: {name}')
        return cls.builders[name](*args, **kwargs)

    @classmethod
    def get_generator(cls, name):
        if name not in cls.generators:
            raise ValueError(f'Unknown generator: {name}')
        return cls.generators[name]()