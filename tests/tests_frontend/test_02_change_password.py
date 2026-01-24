from http import HTTPStatus

import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from pages.login_page import LoginPage
from tests.tests_frontend.frontend_helpers import log_in_user, log_out_and_log_in
from utils.assertions.base_assertions import assert_status_code
from utils.assertions.login_assertions import assert_login
from utils.helper import change_password_payload
from utils.schemas.login_request_schema import LoginRequestSchema
from utils.schemas.login_response_schema import LoginResponseSchema
from utils.validators import validate_response


@allure.feature('Change Password')
@allure.story('Valid forgot your password flow')
@pytest.mark.screenshot
@pytest.mark.video
class TestForgotYourPassword:

    @allure.title('Password changed success toast appears on page')
    def test_user_able_to_change_password(self, register, forgot_your_password_page):

        forgot_your_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD)

        new_data = change_password_payload(register)

        forgot_your_password_page.reset_password(
            **new_data
        )

        forgot_your_password_page.check_password_changed_confirmation_appears_on_page()


    @allure.title('User able to log in with new password')
    def test_user_able_to_log_in_with_new_password(self, unauth_page, forgot_your_password_page, register, login):
        forgot_your_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD)

        new_data = change_password_payload(register)

        forgot_your_password_page.reset_password(
            **new_data
        )

        login_payload = LoginRequestSchema(
            email=new_data['email'],
            password=new_data['new']
        )

        response = login.log_in_user(
            login_payload
        )
        validated_response = validate_response(LoginResponseSchema, response.json())

        assert_login(validated_response, login_payload)

@allure.feature('Change Password')
@allure.story('Valid change password after login flow')
@pytest.mark.screenshot
@pytest.mark.video
class TestChangeYourPasswordAfterLogin:

    @allure.title('Password changed after login success toast appears on page')
    def test_change_password_after_login_toast(self, change_password_after_login_page, register):

        change_password_page, new_user_data = change_password_after_login_page

        change_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD_IN_ACCOUNT)
        change_password_page.change_password_after_login(
            **new_user_data
        )

        change_password_page.check_password_changed_confirmation_appears_on_page()

    @allure.title('User able to change password in account and log in with it')
    def test_user_logs_out_and_logs_in_with_changed_password(self, change_password_after_login_page, login_page, main_page):

        change_password_page, new_user_data = change_password_after_login_page

        change_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD_IN_ACCOUNT)
        change_password_page.change_password_after_login(
            **new_user_data
        )

        log_out_and_log_in(
            current_page=change_password_page,
            login_data=new_user_data
        )

        main_page.check_account_name_matches_email(new_user_data['email'])

