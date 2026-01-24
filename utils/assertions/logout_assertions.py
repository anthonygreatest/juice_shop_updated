import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.logout_resp_schema import LogoutRespSchema
from utils.schemas.register_response_schema import RegisterResponseValidateSchema

logger = get_logger("LOGOUT_ASSERTIONS")

@allure.step('Checking user able to log out')
def assert_user_able_to_log_out(response: LogoutRespSchema, expected: RegisterResponseValidateSchema):

    logger.info('Checking user able to log out')

    assert_match(response.email, expected.data.email, 'email')