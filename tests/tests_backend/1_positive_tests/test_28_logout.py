from http import HTTPStatus

import allure

from utils.assertions.base_assertions import assert_status_code
from utils.assertions.logout_assertions import assert_user_able_to_log_out
from utils.schemas.logout_resp_schema import LogoutRespSchema
from utils.validators import validate_response


@allure.feature('Logout')
@allure.story('Valid logout flow')
@allure.title('User able to log out')
def test_logout(logout, headers_with_auth, register_response):

    response = logout.log_out_user(
        headers=headers_with_auth
    )

    validated_response = validate_response(LogoutRespSchema, response.json())

    assert_status_code(response, HTTPStatus.OK)
    assert_user_able_to_log_out(validated_response, register_response)




