from http import HTTPStatus

import allure

from utils.assertions.base_assertions import assert_status_code
from utils.assertions.change_pass_assertions import assert_password_gets_changed
from utils.assertions.login_assertions import assert_login
from utils.helper import user_logged_in, prepare_change_password_in_acc_payload
from utils.schemas.change_password_resp_schema import ChangePasswordRespSchema
from utils.schemas.login_response_schema import LoginResponseSchema
from utils.validators import validate_response


@allure.feature('Change Password')
@allure.story('Valid change password flow')
class TestChangePassword:

    @allure.title('User able to change password successfully')
    def test_user_able_to_change_password(self, register, change_user_password):

        response, new_password_payload = change_user_password

        validated_response = validate_response(ChangePasswordRespSchema, response.json())

        assert_status_code(response, HTTPStatus.OK)

        assert_password_gets_changed(validated_response, new_password_payload)

    @allure.title('User able to log in with changed password')
    def test_user_able_to_log_in_with_changed_password(self, login, change_user_password):

        response, new_password_payload = change_user_password

        login_data, response = user_logged_in(
            email=new_password_payload.email,
            password=new_password_payload.new,
            login=login
        )

        validated_response = validate_response(LoginResponseSchema, response.json())

        assert_status_code(response, HTTPStatus.OK)

        assert_login(validated_response, login_data)

    def test_user_able_to_change_password_after_login(self, headers_with_auth,
        change_password, registered_user_data, register):

        change_password_in_acc_payload = prepare_change_password_in_acc_payload(
            old_user_password=registered_user_data.password,
            email=registered_user_data.email,
            answer=registered_user_data.security_answer
        )

        response = change_password.change_password_in_account(
            params=change_password_in_acc_payload,
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.OK)