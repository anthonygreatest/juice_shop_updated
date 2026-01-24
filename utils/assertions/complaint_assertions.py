import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.send_complaint_request_schema import SendComplaintRequestSchema
from utils.schemas.send_complaint_resp_schema import SendComplaintRespSchema

logger = get_logger("COMPLAINT_ASSERTIONS")

@allure.step('Checking user complaint gets sent')
def assert_user_complaint_gets_sent(response: SendComplaintRespSchema, expected: SendComplaintRequestSchema):

    logger.info('Checking recycle request gets sent')

    assert_match(response.data.user_id, expected.user_id, 'user id')
    assert_match(response.data.message, expected.message, 'message')