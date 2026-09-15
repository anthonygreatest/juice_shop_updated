import json
import random
from datetime import datetime, timezone
from decimal import Decimal
from http import HTTPStatus
import allure
import pytest
import requests
from httpx import Response
from pypdf import PdfReader

from data.constants import PRODUCTS_LIST
from data.constants2 import DELIVERY_OPTIONS
from data.dataclasses.added_product_data import AddedProductData
from data.dataclasses.change_pass_in_acc import ChangePassInAcc
from data.dataclasses.checkout_data import CheckoutData
from data.dataclasses.delivery_data import DeliveryData
from data.dataclasses.e_wallet_deposit_data import EWalletDepositData
from data.endpoints import Endpoints
from data.factory import DataFactory
from data.generators.generator import BaseFakerGenerator
from data.paths import RECEIPT_PATH, SENSITIVE_PATH
from modules.credit_card_module import CreditCardModule
from utils.schemas.add_address_request_schema import AddAddressSchema
from utils.schemas.add_address_resp_schema import AddAddressRespSchema
from utils.schemas.add_credit_card_request import AddCreditCardRequest
from utils.schemas.add_credit_card_resp_schema import AddCreditCardRespSchema
from utils.schemas.add_to_basket_request_schema import AddToBasketRequestSchema
from utils.schemas.add_to_basket_resp_schema import AddToBasketRespSchema
from utils.schemas.checkout_request_schema import CheckoutRequestSchema
from utils.schemas.checkout_resp_schema import CheckoutRespSchema
from utils.schemas.data_erasure_request_schema import DataErasureRequestSchema
from utils.schemas.data_export_resp_schema import DataExportRespSchema, DataExportRequestSchema
from utils.schemas.delivery_options_resp_schema import DeliveryOptionsRespSchema
from utils.schemas.deluxe_membership_request_schema import DeluxeRequestSchema
from utils.schemas.digital_wallet_request_schema import DigitalWalletRequestSchema
from utils.schemas.get_reviews_resp_schema import GetReviewsRespSchema
from utils.schemas.login_request_schema import LoginRequestSchema
from utils.schemas.login_response_schema import LoginResponseSchema
from utils.schemas.password_schema import RandomPasswordSchema
from utils.schemas.recycle_request_schema import RecycleRequestSchema
from utils.schemas.register_request_schema import RegisterRequestSchema
from utils.schemas.register_response_schema import RegisterResponseValidateSchema
from utils.schemas.robot_resp_schema import RobotRequestSchema
from utils.schemas.send_complaint_request_schema import SendComplaintRequestSchema
from utils.schemas.send_feedback_request_schema import SendFeedbackRequestSchema
from utils.schemas.set_security_question_schema import SetSecuritySchema
from utils.schemas.write_reviews_request_schema import WriteReviewsRequestSchema
from utils.validators import validate_response


def get_questions():

    resp = requests.get(
        url = f'{Endpoints().sec_questions}'
    )
    questions = [q['question'] for q in resp.json()['data']]

    with open(r'/data/constants.py', 'w', encoding='utf-8') as f:
        f.write(f'SECURITY_QUESTIONS = {questions}')

    print('DONE')

def get_deliveries():

    resp = requests.get(
        url = f'{Endpoints().delivery_options}'
    )
    options = resp.json()['data']

    ids = [i['id'] for i in options]

    with open(r'C:\Users\user\PycharmProjects\PythonProject10\data\constants.py', 'a', encoding='utf-8') as f:
        f.write(f'DELIVERY_OPTIONS = {ids}')

    print('DONE')

def list_of_movies_and_books():
    with open(r'C:\Users\user\PycharmProjects\PythonProject10\data\random_films_and_books', 'r', encoding='utf-8') as f:
        books_and_movies = []
        for item in f:
            books_and_movies.append(item.strip())
    with open(r'C:\Users\user\PycharmProjects\PythonProject10\data\constants.py', 'a', encoding='utf-8') as new:
        new.write(f'WORKS_OF_ART = {books_and_movies}')
    print('DONE')

@allure.step('Preparing register request payload')
def prepare_register_payload():
    random_user = DataFactory.get_builder('register').build()

    return RegisterRequestSchema(**random_user)

@allure.step('Preparing security answer payload')
def security_answer_payload(user_id, answer, security_question_id) -> SetSecuritySchema:
    security_ans = {
        'user_id': user_id,
        'answer': answer,
        'security_question_id': security_question_id
    }

    return SetSecuritySchema(**security_ans)

@allure.step('Sending register request')
def registered_user(register) -> tuple[RegisterResponseValidateSchema, RegisterRequestSchema]:
    new_user = prepare_register_payload()

    resp = register.register_new_user(
        data=new_user
    )

    formatted_response = validate_response(RegisterResponseValidateSchema, resp.json())

    return formatted_response, new_user

@allure.step('Sending set security answer request')
def security_answer_set(formatted_response: RegisterResponseValidateSchema, new_user, register):

    security_answer = security_answer_payload(
        user_id=formatted_response.data.id,
        answer=new_user.security_answer,
        security_question_id=new_user.security_question.id
    )

    register.set_security_answer(security_answer)

@allure.step('Sending register and set security answer request')
def register_user_and_set_security_answer(register) -> tuple[RegisterResponseValidateSchema, RegisterRequestSchema]:
    formatted_response, new_user = registered_user(register)
    security_answer_set(formatted_response, new_user, register)

    return formatted_response, new_user

@allure.step('Preparing change password payload')
def change_password_payload(register) -> dict:
    formatted_response, new_user = register_user_and_set_security_answer(register)

    new_password_payload = DataFactory.get_builder('new_pass').build(
        email=new_user.email,
        answer=new_user.security_answer
    )

    return new_password_payload

@allure.step('Getting registered user with changed password')
def registered_user_with_changed_password(register):

    _, new_user = register_user_and_set_security_answer(register)

    new_password_payload = change_password_payload(new_user.email, new_user.security_answer)

    return new_password_payload

@allure.step('Preparing change password in account payload')
def prepare_change_password_in_acc_payload(old_user_password, email, answer):

    new_password_payload = DataFactory.get_builder('new_pass').build(
        email=email,
        answer=answer
    )
    formatted_payload = RandomPasswordSchema(**new_password_payload)

    data = {
        'current': old_user_password,
        'new': formatted_payload.new,
        'repeat': formatted_payload.repeat
    }

    return data

@allure.step('Sending change password request')
def change_password_in_account(change_password, headers, old_user_password, email, answer):

    change_password_in_acc_payload = prepare_change_password_in_acc_payload(
        old_user_password=old_user_password,
        email=email,
        answer=answer
    )

    response = change_password.change_password_in_account(
        params=change_password_in_acc_payload,
        headers=headers
    )

    return response, ChangePassInAcc(**change_password_in_acc_payload)

def prepare_login_payload(email, password):

    data = {
        'email': email,
        'password': password
    }

    return data

@allure.step('Sending login request')
def user_logged_in(email, password, login) -> tuple[LoginRequestSchema, Response]:

    data = prepare_login_payload(email, password)

    login_data = LoginRequestSchema(**data)

    response = login.log_in_user(
        login_data
    )

    return login_data, response

@allure.step('Preparing feedback request payload')
def prepare_customer_feedback_payload(captcha_answer, captcha_id, message, user_id=None):

    data = DataFactory.get_builder('feedback').build(
        user_id=user_id,
        captcha=captcha_answer,
        captcha_id=captcha_id,
        message_type=message
    )

    return SendFeedbackRequestSchema(**data)

@allure.step('Preparing add product to basket payload')
def add_product_to_basket_payload(bid):

    data = DataFactory.get_builder('order').build(bid)

    return AddToBasketRequestSchema(**data)

@allure.step('Adding product to basket')
def product_added_to_basket(login_response, basket, headers_with_auth):
    product_to_be_added = add_product_to_basket_payload(login_response.authentication.bid)

    response = basket.add_to_basket(
        data=product_to_be_added,
        headers=headers_with_auth
    )

    item = None
    if response.status_code == HTTPStatus.OK:
        item = AddToBasketRespSchema(**response.json()).data

    return AddedProductData(
        added_product=product_to_be_added,
        raw_response=response,
        item=item
    )

@allure.step('Changing product quantity in basket')
def change_current_quantity(current_quantity, operation, number):
    if operation == 'add':
        current_quantity += number
    elif operation == 'sub':
        current_quantity -= number
    else:
        raise ValueError('Operation not supported')
    return {
        'quantity': current_quantity
    }

@allure.step('Preparing add address payload for UI')
def add_address_basic_data():

    data = DataFactory.get_builder('delivery_address', ['China', 'Japan']).build()

    return data

@allure.step('Preparing add address request payload')
def add_address_payload():
    data = add_address_basic_data()

    return AddAddressSchema(**data)

@allure.step('Preparing add card request payload')
def add_credit_card_payload() -> AddCreditCardRequest:

    data = DataFactory.get_generator('credit_card').create_credit_card()

    formatted_data = CreditCardModule().create_credit_card_request(data, AddCreditCardRequest)

    return formatted_data

@allure.step('Preparing checkout payload')
def form_checkout_payload(
    address_id: AddAddressRespSchema,
    delivery_method: int,
    payment_id: AddCreditCardRespSchema,
    digital_wallet: bool,
    coupon: str = None):

    data = DataFactory.get_builder('checkout').build(
        address_id,
        delivery_method,
        payment_id,
        digital_wallet,
        coupon
    )

    return CheckoutRequestSchema(**data)

@allure.step('Selecting delivery option')
def select_delivery_option(delivery_options, headers_with_auth):

    selected_option = random.choice(DELIVERY_OPTIONS)

    response = delivery_options.choose_delivery(selected_option['id'], headers_with_auth)

    return DeliveryOptionsRespSchema(**response.json())

@allure.step('Completing order at checkout')
def complete_order(checkout, login_response, headers_with_auth, address_id, delivery_option,
    card_id, digital_wallet, coupon):

    checkout_payload = form_checkout_payload(
        address_id=address_id,
        delivery_method=delivery_option,
        payment_id=card_id,
        digital_wallet=digital_wallet,
        coupon=coupon
    )

    response = checkout.make_order_at_checkout(
        basket_id=login_response.authentication.bid,
        data=checkout_payload,
        headers=headers_with_auth
    )

    return response

@allure.step('Preparing checkout response')
def prepare_checkout_response(checkout_data: CheckoutData):

    return CheckoutRespSchema(**checkout_data.checkout_response.json())

@allure.step('Preparing recycle request payload')
def recycle_payload(user_id, address_id, pickup_needed):

    data = DataFactory.get_builder('recycle').build(
        user_id=user_id,
        address_id=address_id,
        is_pickup=pickup_needed
    )

    return RecycleRequestSchema(**data)

@allure.step('Preparing deposit request payload')
def deposit_to_digital_wallet_payload(payment_id, balance):

    data = DataFactory().get_builder('digital_wallet').build(
        balance=balance,
        payment_id=payment_id
    )

    return DigitalWalletRequestSchema(**data)

@allure.step('Sending deposit request')
def deposit_money_to_e_wallet(payment_id, headers, digital_wallet, balance):

    balance_before = digital_wallet.get_digital_wallet_balance(
        headers=headers
    )

    deposit_payload = deposit_to_digital_wallet_payload(
        payment_id=payment_id,
        balance=balance
    )

    response = digital_wallet.deposit_to_digital_wallet(
        data=deposit_payload,
        headers=headers
    )

    return EWalletDepositData(
        response_raw=response,
        deposit_payload=deposit_payload,
        balance_before_deposit=balance_before
    )

@allure.step('Preparing convenient data export format')
def fix_data_export_format(response):
    user_data = json.loads(response.json()['userData'])
    final_data = response.json()
    final_data['userData'] = user_data

    validated_response = validate_response(DataExportRespSchema, final_data)

    return validated_response

@allure.step('Preparing data export request payload')
def choose_data_export_format(option, answer=None):

    data = {
        'format': option,
        'answer': answer
    }

    return DataExportRequestSchema(**data)

@allure.step('Preparing deluxe membership request payload')
def prepare_deluxe_membership_payload(payment_mode: str, card_id=None):

    data = {
        'payment_id': card_id,
        'payment_mode': payment_mode
    }

    return DeluxeRequestSchema(**data)

@allure.step('Preparing user message request payload')
def prepare_user_message(user_id, message_type):

    data = DataFactory.get_builder('feedback').build(
        user_id=user_id,
        message_type=message_type
    )

    return SendComplaintRequestSchema(**data)

@allure.step('Preparing file for upload request payload')
def prepare_file_for_upload(picture, file_name, caption_comment, headers_with_auth):
    # multipart/form-data, данные передаем в виде кортежа, если нет имени = None

    new_headers = headers_with_auth.copy()

    file = {
        'image': (file_name, open(picture, 'rb'), 'image/png')
    }

    data = {
        'caption': caption_comment
    }

    return file, new_headers, data

@allure.step('Preparing chatbot query request payload')
def prepare_chatbot_query(name):

    data = {
        'action': 'query',
        'query': f'Hey, juicy, I am {name}, can you help me?'
    }

    return RobotRequestSchema(**data)

@allure.step('Generating password pair')
def generate_password_pair():
    return DataFactory.get_generator('password_pair').generate_password_pair()

@allure.step('Preparing deluxe membership request payload')
def get_current_time():
    my_time = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    return my_time

@allure.step('Preparing fake data')
def fake_data_generator():
    return BaseFakerGenerator().faker

@allure.step('Getting product reviews')
def get_product_reviews(reviews, headers, product):

    product_reviews = reviews.get_reviews(
        product,
        headers
    )

    return GetReviewsRespSchema(**product_reviews.json())

@allure.step('Preparing review request payload')
def prepare_review_payload(email):

    data = DataFactory.get_generator('feedback_generator').generate_feedback()

    data_to_send = {
        'author': email,
        'message': data.comment
    }

    return WriteReviewsRequestSchema(**data_to_send)

@allure.step('Preparing data erasure request payload')
def prepare_data_erasure(email, security_answer):

    data = {
        'email': email,
        'securityAnswer': security_answer
    }

    return DataErasureRequestSchema(**data)

@allure.step('Generating new username')
def generate_user_name():
    return DataFactory.get_generator('name').create_name()

@allure.step('Creating invalid fields')
def create_invalid_fields(invalid_fields, data):

    if isinstance(invalid_fields, list):
        for key, value in invalid_fields:
            data[key] = value

    return data

@allure.step('Preparing register request payload')
def prepare_register_payload_for_invalid_data():

    data = prepare_register_payload()

    return data.model_dump(mode='json', by_alias=True, exclude_none=True)

@allure.step('Preparing raw customer feedback request payload')
def prepare_raw_customer_feedback_payload(customer_feedback, headers_with_auth, user_id=None):

    captcha = customer_feedback.get_captcha(
        headers=headers_with_auth
    )

    data = prepare_customer_feedback_payload(
        captcha_answer=captcha.answer,
        captcha_id=captcha.captcha_id,
        user_id=user_id,
        message='feedback'
    )

    return data.model_dump(by_alias=True)

@allure.step('Preparing raw add to basket request payload')
def prepare_raw_add_to_basket_payload(bid, product_id=1, quantity=1):

    data = {
        'ProductId': product_id,
        'quantity': quantity,
        'BasketId': bid
    }

    return data

@allure.step('Preparing missing headers')
def prepare_change_quantity_payload(quantity):

    return {
        'quantity': quantity
    }

@allure.step('Finding product limit per user')
def find_product_limit_per_user(product_id):

    limit = next(product['limit_per_user'] for product in PRODUCTS_LIST if product['id'] == product_id)

    if limit is None:
        pytest.skip('Product has no limit')

    return limit

@allure.step('Preparing raw address request payload')
def prepare_raw_address_payload():

    data = DataFactory.get_builder('delivery_address').build()
    final_data = AddAddressSchema(**data)

    return final_data.model_dump(by_alias=True)

@allure.step('Preparing raw card request payload')
def prepare_raw_card_payload():

    data = add_credit_card_payload()

    return data.model_dump(by_alias=True)

@allure.step('Preparing raw checkout request payload')
def prepare_raw_checkout_payload(address_id, card_id, digital_wallet, coupon=None):

    selected_option = random.choice(DELIVERY_OPTIONS)

    checkout_payload = form_checkout_payload(
        address_id=address_id,
        delivery_method=selected_option,
        payment_id=card_id,
        digital_wallet=digital_wallet,
        coupon=coupon
    )

    return checkout_payload.model_dump(by_alias=True)

@allure.step('Preparing raw checkout request payload')
def prepare_checkout_with_missing_fields(schema, data, missing_field):

    if schema == 'inner':
        data['orderDetails'].pop(missing_field)
    else:
        data.pop(missing_field)

    return data


@allure.step('Preparing correct recycle payload format')
def prepare_recycle_payload_for_invalid_data(user_id, address_id, pickup_needed=False):

    data = recycle_payload(user_id, address_id, pickup_needed)

    return data.model_dump(mode='json', by_alias=True, exclude_none=True)

@allure.step('Preparing raw card request payload')
def prepare_raw_deposit_payload(payment_id, balance):

    data = deposit_to_digital_wallet_payload(payment_id, balance)

    return data.model_dump(by_alias=True)

@allure.step('Preparing raw card request payload')
def prepare_raw_deluxe_membership_payload(payment_mode, card_id=None):

    data = prepare_deluxe_membership_payload(
        payment_mode=payment_mode,
        card_id=card_id
    )

    return data.model_dump(by_alias=True)

@allure.step('Sending create new user request payload')
def prepare_fresh_user(register, login):

    register_response, new_user = register_user_and_set_security_answer(register)

    login_data, response = user_logged_in(
        new_user.email,
        new_user.password,
        login
    )

    login_response = LoginResponseSchema(**response.json())

    headers = {'Authorization': f'Bearer {login_response.authentication.token}'}

    return headers

@allure.step('Preparing complaint message request payload')
def prepare_complaint_message(user_id, message_type):

    data = prepare_user_message(
        user_id=user_id,
        message_type=message_type
    )

    return data.model_dump(by_alias=True)

@allure.step('Preparing review request payload')
def prepare_review_to_like(comment_id):

    favorite_review = {
        'id': comment_id
    }

    return favorite_review

@allure.step('Preparing review request payload')
def prepare_raw_review_payload(email):

    data = prepare_review_payload(email)

    return data.model_dump(by_alias=True)

@allure.step('Preparing raw chatbot request payload')
def raw_chatbot_query(name='Tony'):

    data = prepare_chatbot_query(name)

    return data.model_dump(by_alias=True)

def choose_data_export_format_raw(option='1', answer=None):

    data = choose_data_export_format(
        option=option,
        answer=answer
    )

    return data.model_dump(by_alias=True)

def get_ids_of_products():

    resp = requests.get(
        url='http://localhost:3000/api/Quantitys'
    )

    products = resp.json()['data']

    resp2 = requests.get(
        url='http://127.0.0.1:3000/rest/products/search?q='
    )

    product_names = {i['id']: (i['name'], i['price']) for i in resp2.json()['data']}
    print(product_names)

    with open(r'C:\Users\user\PycharmProjects\PythonProject12\data\constants2.py', 'w', encoding='utf-8') as f:
        products_list = []
        for i in products:
            products_list.append({'id': i['ProductId'], 'quantity': i['quantity'], 'limit_per_user': i['limitPerUser']})

        for item in products_list:
            if item['id'] in product_names:
                item['name'] = product_names[item['id']][0]
                item['price'] = product_names[item['id']][1]

        f.write(f'NEW_PRODUCTS = {products_list}')

    print('DONE')

def select_delivery_speed():

    selected_option = random.choice(DELIVERY_OPTIONS)

    return DeliveryData(
        delivery_date=selected_option['eta'],
        delivery_price=Decimal(str(selected_option['price']))
    )

def get_receipt_data(receipt):

    with open(RECEIPT_PATH, 'wb') as file:
        file.write(receipt.content)

    reader = PdfReader(RECEIPT_PATH)
    receipt_text = reader.pages[0].extract_text()

    return receipt_text

def record_password_and_email(password, email):

    with open(SENSITIVE_PATH, 'w') as f:
        f.write(
            f'PASSWORD={password}'
            f'\nEMAIL={email}'
        )