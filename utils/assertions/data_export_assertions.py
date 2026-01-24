import allure

from data.dataclasses.checkout_data import CheckoutData
from data.dataclasses.exported_data import ExportedData
from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.checkout_resp_schema import CheckoutRespSchema
from utils.schemas.data_export_resp_schema import DataExportRespSchema, DataExportRespSchemaInside

logger = get_logger("DATA_EXPORT_ASSERTIONS")

@allure.step('Checking user order tracking data present in data export')
def assert_export_data_matches_user_data(response: DataExportRespSchema,
    expected: CheckoutRespSchema):

    logger.info('Checking user order tracking data present in data export')

    assert any(order.order_id == expected.order_confirmation for order in response.user_data.orders)


@allure.step('Checking user order data present in data export')
def check_exported_data_matches_user_data(exported_data: list[ExportedData],
    expected_user_data: CheckoutData):

    logger.info('Checking user order data present in data export')

    expected_total_price = expected_user_data.product_name_and_price.product_price + expected_user_data.delivery_selected.data.price

    assert any(order.name == expected_user_data.product_name_and_price.product_name and
               order.total_price == expected_total_price and
               order.order_id == expected_user_data.checkout_response.json()['orderConfirmation'] and
               order.delivery_date == expected_user_data.delivery_selected.data.eta for order in exported_data)