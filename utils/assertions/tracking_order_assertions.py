import allure

from data.dataclasses.checkout_data import CheckoutData
from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.add_address_resp_schema import AddAddressRespSchema
from utils.schemas.add_credit_card_resp_schema import AddCreditCardRespSchema
from utils.schemas.add_to_basket_request_schema import AddToBasketRequestSchema
from utils.schemas.checkout_resp_schema import CheckoutRespSchema
from utils.schemas.delivery_options_resp_schema import DeliveryOptionsRespSchema
from utils.schemas.get_order_history_schema import GetOrderHistoryListSchema
from utils.schemas.login_response_schema import LoginResponseSchema

logger = get_logger("TRACKING_ORDER_ASSERTIONS")

@allure.step('Checking tracking order match')
def assert_tracking_order_data_matches_order_data(
    response: GetOrderHistoryListSchema,
    expected_product_data: AddToBasketRequestSchema,
    expected_payment_data: AddCreditCardRespSchema,
    expected_address_data: AddAddressRespSchema,
    expected_delivery_data: DeliveryOptionsRespSchema,
    tracking_order: CheckoutRespSchema):

    logger.info('Checking tracking order match')

    matched = next(
        (order for order in response.data if order.order_id == tracking_order.order_confirmation),
        None
    )

    assert matched, f'Order with {tracking_order} not found'

    assert_match(matched.products[0].id, expected_product_data.product_id, 'product id')
    assert_match(matched.products[0].quantity, expected_product_data.quantity, 'quantity')
    assert_match(int(matched.address_id), expected_address_data.data.id, 'address id')
    assert_match(int(matched.payment_id), expected_payment_data.data.id, 'payment id')
    assert_match(matched.delivery_price, expected_delivery_data.data.price, 'delivery price')

@allure.step('Checking print order confirmation url match')
def assert_print_order_confirmation_url_matches_expected(actual_url: str, expected_url: str):

    logger.info('Checking print order confirmation url match')

    assert_match(actual_url, expected_url, 'print order confirmation url')

@allure.step('Checking twitter repost links match')
def assert_twitter_repost_link_matches_expected(actual_url: str, expected_url: str):
    logger.info('Checking twitter repost links match')

    assert_match(actual_url, expected_url, 'twitter repost link')

@allure.step('Checking outer source link matches expected')
def assert_outer_source_link_matches_expected(actual_url: str, expected_url: str):
    logger.info('Checking outer source link matches expected')

    assert expected_url in actual_url

@allure.step('Checking receipt data matches expected')
def assert_receipt_data_matches_expected(receipt_data: str, email_data: LoginResponseSchema, checkout_data: CheckoutData):
    logger.info('Checking receipt data matches expected')

    product_name = checkout_data.product_name_and_price.product_name.replace('OW', '').replace('WASP', '')

    assert product_name in receipt_data
    assert checkout_data.checkout_response.json()['orderConfirmation'] in receipt_data
    assert str(checkout_data.product_name_and_price.product_price) in receipt_data
    assert str(checkout_data.delivery_selected.data.price) in receipt_data
    assert str(checkout_data.delivery_selected.data.price + checkout_data.product_name_and_price.product_price) in receipt_data
    assert str(email_data.authentication.umail) in receipt_data



