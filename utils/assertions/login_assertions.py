import allure

from utils.assertions.base_assertions import assert_match
from utils.clients.event_hooks import get_logger
from utils.schemas.login_request_schema import LoginRequestSchema
from utils.schemas.login_response_schema import LoginResponseSchema


logger = get_logger("LOGIN_ASSERTIONS")

@allure.step('Checking user logged in')
def assert_login(response: LoginResponseSchema, expected: LoginRequestSchema):

    logger.info('Checking user logged in')

    assert_match(response.authentication.umail, expected.email, 'email')