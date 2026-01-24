import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.add_address_resp_schema import AddAddressRespSchema
from utils.schemas.add_credit_card_resp_schema import AddCreditCardRespSchema
from utils.schemas.add_to_basket_request_schema import AddToBasketRequestSchema
from utils.schemas.checkout_resp_schema import CheckoutRespSchema
from utils.schemas.delivery_options_resp_schema import DeliveryOptionsRespSchema
from utils.schemas.get_order_history_schema import GetOrderHistoryListSchema

logger = get_logger("ORDER_HISTORY_ASSERTIONS")

@allure.step('Checking order history match')
def assert_order_history_matches_order_data(
    response: GetOrderHistoryListSchema,
    expected_product_data: AddToBasketRequestSchema,
    expected_payment_data: AddCreditCardRespSchema,
    expected_address_data: AddAddressRespSchema,
    expected_delivery_data: DeliveryOptionsRespSchema,
    tracking_order: CheckoutRespSchema):

    logger.info('Checking order history match')

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


