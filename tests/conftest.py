import random
from pathlib import Path

import allure
import pytest
from httpx import Client

from config import Settings
from data.constants import DELIVERY_OPTIONS, PRODUCTS_LIST
from data.dataclasses.checkout_data import CheckoutData
from data.dataclasses.created_address_data import CreatedAddressData
from data.dataclasses.created_card_data import CreatedCardData
from data.dataclasses.dataclass import UnlikedReview
from data.dataclasses.login_data import LoginData
from data.dataclasses.review_data import ReviewData
from tests.tests_frontend.frontend_helpers import find_product_by_id

from utils.clients.api_client import Register, ChangePassword, Login, CustomerFeedback, Basket, Address, \
    DeliveryOptions, CreditCard, Checkout, TrackingOrder, OrderHistory, Recycle, DigitalWallet, DataExport, \
    DeluxeMembership, Complaints, PhotoWall, Chatbot, Logout, Reviews, DataErasure
from utils.clients.event_hooks import log_request_event_hook, log_response_event_hook
from utils.helper import register_user_and_set_security_answer, \
    user_logged_in, add_address_payload, \
    add_credit_card_payload, complete_order, deposit_money_to_e_wallet, select_delivery_option, \
    choose_data_export_format, prepare_file_for_upload, get_product_reviews, \
    prepare_review_payload, generate_user_name, registered_user_with_changed_password, \
    prepare_customer_feedback_payload, product_added_to_basket, recycle_payload, prepare_checkout_response
from utils.raw_api_client import RawAPIClient
from pytest import Item
from utils.schemas.add_address_resp_schema import AddAddressRespSchema
from utils.schemas.add_credit_card_resp_schema import AddCreditCardRespSchema
from utils.schemas.like_review_resp_schema import LikeReviewRequestSchema
from utils.schemas.login_response_schema import LoginResponseSchema
from utils.schemas.password_schema import RandomPasswordSchema

@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(item: Item):
    yield
    allure.dynamic.title(' '.join(item.name.split('_')[1:]).capitalize())

#
# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     durations = []
#     for test in terminalreporter.stats.get('passed', []):
#         durations.append([test.nodeid, test.duration])
#     for test in terminalreporter.stats.get('failed', []):
#         durations.append([test.nodeid, test.duration])
#     for test in terminalreporter.stats.get('skipped', []):
#         durations.append([test.nodeid, test.duration])
#     config.cache.set('test_durations', durations)
#
# @pytest.hookimpl(tryfirst=True)
# def pytest_collection_modifyitems(session, config, items):
#     durations = config.cache.get('test_durations', [])
#     durations_dict = {nodeid: duration for nodeid, duration in durations}
#     items.sort(key=lambda item: durations_dict.get(item.nodeid, 0), reverse=True)
#
# class FifoBasedScheduler(LoadScopeScheduling):
#
#     def _split_scope(self, nodeid: str) -> str:
#         return nodeid
#
# @pytest.hookimpl(tryfirst=True)
# def pytest_xdist_make_scheduler(config, log):
#     return FifoBasedScheduler(config, log)

@pytest.fixture(scope='session')
def raw_api_client(http_client):
    return RawAPIClient(http_client)

@pytest.fixture(scope='session')
def api_settings() -> Settings:
    return Settings()

@pytest.fixture(scope='session')
def http_client(api_settings: Settings) -> Client:
    settings = api_settings.shop_http_client
    return Client(
        timeout=settings.timeout,
        base_url=settings.client_url,
        event_hooks={
            'request': [log_request_event_hook],
            'response': [log_response_event_hook]
        }
    )

@pytest.fixture(scope='session')
def register(http_client: Client) -> Register:
    return Register(
        http_client
    )

@pytest.fixture(scope='session')
def change_password(http_client):
    return ChangePassword(
        http_client
    )

@pytest.fixture(scope='session')
def login(http_client):
    return Login(
        http_client
    )

@pytest.fixture
def change_user_password(register, change_password):

    new_password_payload = registered_user_with_changed_password(register)

    formatted_payload = RandomPasswordSchema(**new_password_payload)

    response = change_password.change_password(
        data=formatted_payload
    )

    return response, formatted_payload

@pytest.fixture(scope='session')
def logged_in_user(register, login):
    register_response, new_user = register_user_and_set_security_answer(register)

    login_data, response = user_logged_in(
        new_user.email,
        new_user.password,
        login
    )

    login_response = LoginResponseSchema(**response.json())

    headers = {'Authorization': f'Bearer {login_response.authentication.token}'}

    headers_with_auth = headers.copy()

    return LoginData(
        headers_with_auth=headers_with_auth,
        register_response=register_response,
        registered_user_data=new_user,
        login_response=login_response
    )

@pytest.fixture
def send_feedback(customer_feedback):

    def _send_feedback(headers, register_response):

        captcha = customer_feedback.get_captcha(
            headers=headers
        )

        feedback_to_send = prepare_customer_feedback_payload(
            captcha_answer=captcha.answer,
            captcha_id=captcha.captcha_id,
            user_id=register_response.data.id,
            message='feedback'
        )

        response = customer_feedback.send_feedback(
            data=feedback_to_send,
            headers=headers
        )

        return response, feedback_to_send
    return _send_feedback

@pytest.fixture(scope='session')
def headers_with_auth(logged_in_user):
    return logged_in_user.headers_with_auth

@pytest.fixture(scope='session')
def register_response(logged_in_user):
    return logged_in_user.register_response

@pytest.fixture(scope='session')
def registered_user_data(logged_in_user):
    return logged_in_user.registered_user_data

@pytest.fixture(scope='session')
def login_response(logged_in_user):
    return logged_in_user.login_response

@pytest.fixture(scope='session')
def customer_feedback(http_client):
    return CustomerFeedback(
        http_client
    )

@pytest.fixture(scope='session')
def basket(http_client):
    return Basket(
        http_client
    )

@pytest.fixture(scope='session')
def address(http_client):
    return Address(
        http_client
    )

@pytest.fixture(scope='session')
def delivery_options(http_client):
    return DeliveryOptions(
        http_client
    )

@pytest.fixture
def add_product_to_basket(request, basket):

    created = []

    def _add_product_to_basket(headers, login_response):

        data = product_added_to_basket(
            login_response=login_response,
            basket=basket,
            headers_with_auth=headers
        )

        created.append({
            'id': data.item.id,
            'headers': headers
        })

        return data

    yield _add_product_to_basket

    if request.node.get_closest_marker('delete_product'):
        for item in created:
            basket.delete_product_from_basket(
                order_id=item['id'],
                headers=item['headers']
            )

@pytest.fixture
def create_address(request, address):

    created = []

    def _create_address(headers):

        address_to_be_added = add_address_payload()

        response = address.create_address(
            data=address_to_be_added,
            headers=headers
        )
        created.append({
            'address_id': response.json()['data']['id'],
            'headers': headers
        })

        formatted_response = AddAddressRespSchema(**response.json())

        return CreatedAddressData(
            response_raw=response,
            address_payload=address_to_be_added,
            added_address=formatted_response
        )
    yield _create_address

    if 'delete_address' in request.keywords:
        for address_data in created:
            address.delete_address(
                address_id=address_data['address_id'],
                headers=address_data['headers']
            )

@pytest.fixture(scope='session')
def credit_card(http_client):
    return CreditCard(
        http_client
    )


@pytest.fixture
def create_credit_card(request, credit_card):

    created = []

    def _create_credit_card(headers):

        card_to_be_added = add_credit_card_payload()

        response = credit_card.add_credit_card(
            data=card_to_be_added,
            headers=headers
        )

        created.append({
            'card_id': response.json()['data']['id'],
            'headers': headers
        })

        formatted_response = AddCreditCardRespSchema(**response.json())

        return CreatedCardData(
            response_raw=response,
            card_payload=card_to_be_added,
            added_card=formatted_response
        )

    yield _create_credit_card

    if request.node.get_closest_marker('delete_card'):
        for card in created:
            credit_card.delete_credit_card(
                card_id=card['card_id'],
                headers=card['headers']
            )

@pytest.fixture(scope='session')
def checkout(http_client):
    return Checkout(
        http_client
    )

@pytest.fixture(scope='session')
def tracking_order(http_client):
    return TrackingOrder(
        http_client
    )

@pytest.fixture(scope='session')
def order_history(http_client):
    return OrderHistory(
        http_client
    )

@pytest.fixture(scope='session')
def recycling(http_client):
    return Recycle(
        http_client
    )

@pytest.fixture(scope='session')
def digital_wallet(http_client):
    return DigitalWallet(
        http_client
    )

@pytest.fixture
def checkout_factory(checkout, add_product_to_basket,
    create_address, create_credit_card, digital_wallet, delivery_options):

    def _checkout(e_wallet, headers, login_response, coupon=None):

        product_to_be_added = add_product_to_basket(headers=headers, login_response=login_response).added_product
        product_name_and_price = find_product_by_id(product_id=product_to_be_added.product_id)

        address_to_be_added = create_address(headers).added_address
        card_to_be_added = create_credit_card(headers).added_card

        delivery_selected = select_delivery_option(delivery_options, headers)

        deposit_money_to_e_wallet(
            card_to_be_added.data.id,
            headers,
            digital_wallet,
            'random'
        )

        balance_before = digital_wallet.get_digital_wallet_balance(
            headers=headers
        )

        checkout_response = complete_order(
            checkout=checkout,
            login_response=login_response,
            headers_with_auth=headers,
            address_id=address_to_be_added.data.id,
            delivery_option=delivery_selected.data.id,
            card_id=card_to_be_added.data.id,
            digital_wallet=e_wallet,
            coupon=coupon
        )

        return CheckoutData(
            checkout_response=checkout_response,
            balance_before=balance_before,
            selected_product=product_to_be_added,
            address_created=address_to_be_added,
            card_created=card_to_be_added,
            delivery_selected=delivery_selected,
            product_name_and_price=product_name_and_price
        )

    return _checkout

@pytest.fixture
def recycle_factory(recycling, create_address, headers_with_auth):

    def _recycle_factory(pickup_needed):
        address_to_be_added = create_address(headers_with_auth).added_address

        recycle_data = recycle_payload(
            user_id=address_to_be_added.data.user_id,
            address_id=address_to_be_added.data.id,
            pickup_needed=pickup_needed
        )

        response = recycling.recycle(
            data=recycle_data,
            headers=headers_with_auth
        )

        return response, recycle_data

    return _recycle_factory

@pytest.fixture(scope='session')
def export_data(http_client):
    return DataExport(
        http_client
    )

@pytest.fixture(scope='session')
def deluxe_membership(http_client):

    return DeluxeMembership(
        http_client
    )

@pytest.fixture(scope='session')
def complaints(http_client):
    return Complaints(
        http_client
    )

@pytest.fixture(scope='session')
def photo_wall(http_client):
    return PhotoWall(
        http_client
    )

@pytest.fixture(scope='session')
def chatbot(http_client):
    return Chatbot(
        http_client
    )

@pytest.fixture(scope='session')
def logout(http_client):
    return Logout(
        http_client
    )

@pytest.fixture(scope='session')
def reviews(http_client):
    return Reviews(
        http_client
    )


@pytest.fixture
def upload_photo(headers_with_auth, photo_wall):
    def _upload_photo(picture, file_name, caption_comment):

        file, new_headers, data = prepare_file_for_upload(
            picture=picture,
            file_name=file_name,
            caption_comment=caption_comment,
            headers_with_auth=headers_with_auth
        )

        response = photo_wall.upload_photo(
            files=file,
            headers=new_headers,
            data=data
        )

        return response
    return _upload_photo


@pytest.fixture(scope='session')
def stub_profile_name(headers_with_auth):

    new_name = generate_user_name()

    class StubResponse:

        status_code = 200
        headers = headers_with_auth

        def json(self):
            return {'username': new_name}

    return StubResponse()

@pytest.fixture
def get_unliked_review(reviews, headers_with_auth, register_response):

    email = register_response.data.email

    comment_to_like = None
    product_id = None
    likes = None

    for product in range(1, len(PRODUCTS_LIST)):

        selected_product_reviews = get_product_reviews(
            reviews,
            headers_with_auth,
            product
        )

        if selected_product_reviews.data:

            for comment in selected_product_reviews.data:
                if comment.likes_count == 0 and email not in comment.liked_by:
                    comment_to_like = comment.id
                    product_id = product
                    likes = comment.likes_count
                    break

        if comment_to_like:
            break

    return UnlikedReview(
        selected_product_reviews=selected_product_reviews,
        comment_to_like=comment_to_like,
        product_id=product_id,
        num_of_likes=likes
    )


@pytest.fixture
def leave_a_like_under_review(reviews, get_unliked_review, headers_with_auth):

    favorite_review  = {
        'id': get_unliked_review.comment_to_like
    }

    formatted_review = LikeReviewRequestSchema(**favorite_review)

    response = reviews.like_a_review(
        data=formatted_review,
        headers=headers_with_auth
    )

    return response

@pytest.fixture
def write_review(headers_with_auth, reviews, login_response):

    email = login_response.authentication.umail

    selected_product = random.choice(PRODUCTS_LIST)['id']

    data_to_send = prepare_review_payload(
        email=email
    )

    response = reviews.write_review(
        data=data_to_send,
        product_id=selected_product,
        headers=headers_with_auth
    )

    return ReviewData(
        response=response,
        email=email,
        reviewed_product=selected_product,
        message=data_to_send.message
    )

@pytest.fixture(scope='session')
def data_erasure(http_client):
    return DataErasure(
        http_client
    )


@pytest.fixture
def export_user_data(headers_with_auth, export_data, checkout_factory, login_response):
    def _export_user_data(captcha_answer=None):

        checkout_data = checkout_factory(e_wallet=False, headers=headers_with_auth, login_response=login_response)
        checkout_response = prepare_checkout_response(checkout_data)

        data = choose_data_export_format(option='1', answer=captcha_answer)

        data_export_response = export_data.request_data_export(
            data=data,
            headers=headers_with_auth
        )

        return data_export_response, checkout_response

    return _export_user_data
