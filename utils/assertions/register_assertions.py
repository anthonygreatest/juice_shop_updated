import allure
from httpx import Response

from utils.assertions.base_assertions import assert_match
from utils.clients.event_hooks import get_logger
from utils.schemas.register_request_schema import RegisterRequestSchema
from utils.schemas.register_response_schema import RegisterResponseValidateSchema
from utils.schemas.security_question_resp_schema import SecurityQuestionRespSchema
from utils.schemas.set_security_question_schema import SetSecuritySchema

logger = get_logger("REGISTER_ASSERTIONS")

@allure.step('Checking user registered')
def assert_user_registered(response: RegisterResponseValidateSchema, expected:RegisterRequestSchema):

    logger.info('Checking user registered')

    assert_match(response.data.email, expected.email, 'email')

@allure.step('Checking security answer gets sent')
def assert_security_answer_gets_sent(response: SecurityQuestionRespSchema, expected: SetSecuritySchema):

    logger.info('Checking security answer gets sent')

    assert_match(response.data.user_id, expected.user_id, 'user id')
    assert_match(response.data.security_question_id, expected.security_question_id, 'security question id')


@allure.step('Checking user not able to register again')
def assert_user_not_able_to_register_again(response: Response, error_message: str):

    logger.info('Checking user not able to register again')

    assert response.json()['errors'][0]['message'] == error_message
