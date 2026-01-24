import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.recycle_request_schema import RecycleRequestSchema
from utils.schemas.recycle_resp_schema import RecycleRespSchema


logger = get_logger("RECYCLE_ASSERTIONS")

@allure.step('Checking recycle request gets sent')
def assert_recycle_request_gets_sent(response: RecycleRespSchema, expected: RecycleRequestSchema):

    logger.info('Checking recycle request gets sent')

    assert_match(response.data.address_id, expected.address_id, 'address id')
    assert_match(response.data.user_id, expected.user_id, 'user id')
    assert_match(response.data.quantity, expected.quantity, 'quantity')
    assert_match(response.data.is_pickup, expected.is_pickup, 'pickup needed')
    assert_match(response.data.date, expected.date, 'pickup date')