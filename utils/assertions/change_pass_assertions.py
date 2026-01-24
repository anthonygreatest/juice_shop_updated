import allure

from utils.assertions.base_assertions import assert_match
from utils.clients.event_hooks import get_logger
from utils.schemas.change_password_resp_schema import ChangePasswordRespSchema
from utils.schemas.password_schema import RandomPasswordSchema

logger = get_logger("CHANGE_PASSWORD_ASSERTIONS")

@allure.step('Checking password_gets_changed')
def assert_password_gets_changed(response: ChangePasswordRespSchema, expected: RandomPasswordSchema):

    logger.info('Checking password_gets_changed')

    assert_match(response.user.email, expected.email, 'email')
