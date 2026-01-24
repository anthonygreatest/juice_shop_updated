import random
from datetime import datetime, timezone
from decimal import Decimal

from faker import Faker



from data.generators.address_generator import address_generator
from data.generators.order_generator import order_generator
from data.generators.pass_generator import PasswordGenerator
from data.generators.user_generator import user_generator

faker = Faker()

class BaseBuilder:

    def __init__(self):
        self.result = {}

    def set(self, key, value):
        self.result[key] = value
        return self

    def build(self, *args, **kwargs):
        return self.result


class UserBuilder(BaseBuilder):

    def __init__(self):
        super().__init__()
        self.result = user_generator()

    def set_email(self, email):
        return self.set('email', email)

    def set_password(self, password):
        return self.set('password', password)

    def set_repeat_password(self, repeat_pass):
        return self.set('password_repeat', repeat_pass)

    def _auto_fill(self):

        if self.result['email'] is None:
            self.result['email'] = faker.email()

        if self.result['password'] is None and self.result['password_repeat'] is None:
            password = faker.password()
            self.result['password'] = password
            self.result['password_repeat'] = password

        return self

    def build(self, *args, **kwargs):
        self._auto_fill()

        return super().build()

class BuilderPassReset(BaseBuilder):

    def __init__(self):
        super().__init__()

    def set_email(self, email):
        return self.set('email', email)

    def set_answer(self, answer):
        return self.set('answer', answer)

    def set_new_password(self, new_password):
        return self.set('new', new_password)

    def set_repeat_password(self, repeat_password):
        return self.set('repeat', repeat_password)

    def _generate_pass(self, answer=None, email=None):
        if self.result.get('new') is None and self.result.get('repeat') is None:
            self.result = PasswordGenerator().pass_generator()
            self.result['email'] = email
            self.result['answer'] = answer
        else:
            self.result['email'] = email
            self.result['answer'] = answer
        return self

    def build(self, answer=None, email=None):
        self._generate_pass(answer, email)
        return super().build()


class BuilderOrder(BaseBuilder):

    def __init__(self):
        super().__init__()

    def set_product_id(self, product_id):
        return self.set('product_id', product_id)

    def set_quantity(self, quantity):
        return self.set('quantity', quantity)

    def set_basket_id(self, basket_id):
        return self.set('basket_id', basket_id)

    def generate_random(self, basket_id):

        if self.result.get('product_id') is None:

            self.result = order_generator(basket_id)
        else:
            self.result['basket_id'] = basket_id


        return self

    def build(self, basket_id):
        self.generate_random(basket_id)
        return super().build()


class BuilderAddress(BaseBuilder):

    def __init__(self, excluded=None):
        super().__init__()
        self.result = address_generator(excluded)

    def set_full_name(self, full_name):
        return self.set('full_name', full_name)

    def set_st_address(self, st_address):
        return self.set('street_address', st_address)

    def set_mobile_num(self, mobile_num):
        return self.set('mobile_num', mobile_num)

    def set_zip(self, zip_code):
        return self.set('zip_code', zip_code)

    def set_country(self, country):
        return self.set('country', country)

    def set_city(self, city):
        return self.set('city', city)

    def set_state(self, state):
        return self.set('state', state)

    def _auto_fill(self):
        if self.result['country'] == 'USA':
            self.result['state'] = faker.state()
        return self

    def build(self, *args, **kwargs):

        self._auto_fill()

        return super().build()


class BuilderCheckout(BaseBuilder):

    def __init__(self):
        super().__init__()
        self.result = {
            'order_details': {

            }
        }

    def set_coupon(self, coupon):
        return self.set('coupon', coupon)

    def set_address_id(self, address_id):
        self.result['order_details']['address_id'] = address_id
        return self

    def set_delivery_method(self, delivery_method):
        self.result['order_details']['delivery_method_id'] = delivery_method
        return self

    def set_payment_id(self, payment_id):
        self.result['order_details']['payment_id'] = payment_id
        return self

    def _auto_fill(self, address_id, delivery_method, payment_id, digital_wallet, coupon):

        self.result['coupon_data'] = coupon
        self.result['order_details']['address_id'] = str(address_id)
        self.result['order_details']['delivery_method_id'] = str(delivery_method)
        if digital_wallet:
            self.result['order_details']['payment_id'] = 'wallet'
        else:
            self.result['order_details']['payment_id'] = str(payment_id)

        return self

    def build(self, address_id, delivery_method, payment_id, digital_wallet, coupon):

        self._auto_fill(address_id, delivery_method, payment_id, digital_wallet, coupon)

        return super().build()


class BuilderFeedback(BaseBuilder):

    def __init__(self):
        super().__init__()

    def set_rating(self, rating):
        return self.set('rating', rating)

    def set_comment(self, comment):
        return self.set('comment', comment)

    def set_captcha(self, captcha):
        return self.set('captcha', captcha)

    def set_captcha_id(self, captcha_id):
        return self.set('captcha_id', captcha_id)

    def set_user_id(self, user_id):
        return self.set('user_id', user_id)

    def set_complaint(self, complaint):
        return self.set('message', complaint)

    def _auto_fill(self, user_id=None, captcha=None, captcha_id=None, message_type=None):
        if message_type == 'feedback':
            self.result['comment'] = faker.sentence()
            self.result['rating'] = random.randint(1, 5)
            self.result['captcha'] = captcha
            self.result['captcha_id'] = captcha_id
            self.result['user_id'] = user_id
        elif message_type == 'complaint':
            self.result['user_id'] = user_id
            self.result['message'] = faker.sentence()
        return self

    def build(self, *args, **kwargs):

        self._auto_fill(*args, **kwargs)

        return super().build()

class BuilderRecycle(BaseBuilder):

    def __init__(self):
        super().__init__()

    def set_user_id(self, user_id):
        return self.set('user_id', user_id)

    def set_address_id(self, address_id):
        return self.set('address_id', address_id)

    def set_quantity(self, quantity):
        return self.set('quantity', quantity)

    def set_date(self, date):
        return self.set('date', date)

    def set_is_pickup(self, is_pickup):
        return self.set('is_pickup', is_pickup)

    def generate_data(self, user_id=None, address_id=None, is_pickup=False):

        if self.result.get('user_id') is None:

            if is_pickup:
                self.result['user_id'] = user_id
                self.result['address_id'] = address_id
                self.result['quantity'] = random.randint(100, 1000)
                self.result['is_pickup'] = True
                self.result['date'] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
                #.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            else:
                self.result['user_id'] = user_id
                self.result['address_id'] = address_id
                self.result['quantity'] = random.randint(1, 100)
        
        return self


    def build(self, user_id=None, address_id=None, is_pickup=None):

        self.generate_data(user_id, address_id, is_pickup)
        return super().build()

class DigitalWalletBuilder(BaseBuilder):

    def __init__(self):
        super().__init__()

    def set_balance(self, balance):
        return self.set('balance', balance)

    def generate_data(self, balance, payment_id):

        self.result['payment_id'] = payment_id
        if balance == 'random':
            self.result['balance'] = Decimal(random.randint(10, 1000))
        elif balance == 'deluxe membership':
            self.result['balance'] = 48
        else:
            self.result['balance'] = balance

        return self

    def build(self, balance, payment_id):
        self.generate_data(balance, payment_id)
        return super().build()


class ReviewBuilder(BaseBuilder):

    def __init__(self):
        super().__init__()

    def generate(self, email=None):
        if email is None:
            self.result['email'] = faker.email()
        else:
            self.result['email'] = email
        self.result['comment'] = faker.sentence()

    def build(self, email):
        self.generate(email)
        return super().build()

