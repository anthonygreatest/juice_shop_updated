import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.delivery_options_resp_schema import DeliveryOptionsRespSchema

logger = get_logger("DELIVERY_OPTIONS_ASSERTIONS")

@allure.step('Checking delivery option gets selected')
def assert_delivery_option_selected(response: DeliveryOptionsRespSchema, delivery_option: int):

    logger.info('Checking delivery option gets selected')

    assert_match(response.data.id, delivery_option, 'delivery option id')
