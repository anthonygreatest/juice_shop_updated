import json

import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from pages.login_page import LoginPage
from tests.tests_frontend.frontend_helpers import log_in_user
from utils.helper import prepare_register_payload, prepare_login_payload


@pytest.mark.screenshot
@allure.feature('Login')
@allure.story('Invalid login flow')
class TestLoginNegative:

    @allure.title('Unregistered user not able to log in')
    def test_log_in_unregistered_user(self, login_page):

        user_data = prepare_register_payload()

        login_page.open(PlaywrightEndpoints.LOGIN)
        login_page = log_in_user(
            user_data,
            login_page
        )
        login_page.click_login_btn()

        login_page.check_invalid_data_error_appears_on_page()

    @allure.title('User not registered with invalid or missing data')
    @pytest.mark.parametrize('missing_field, expected_error', [
        ('email', LoginPage.EMPTY_EMAIL),
        ('password', LoginPage.EMPTY_PASSWORD)
    ])
    @allure.title('User not able to log in with empty data')
    def test_log_in_with_empty_data(self, login_page, missing_field, expected_error):

        user_data = prepare_register_payload()
        invalid_data = prepare_login_payload(
            user_data.email,
            user_data.password
        )
        invalid_data.pop(missing_field)

        login_page.open(PlaywrightEndpoints.LOGIN)
        login_page = log_in_user(
            invalid_data,
            login_page
        )
        login_page.login_form.leave_fields_empty(missing_field)

        login_page.check_login_button_remains_disabled()
        login_page.check_empty_field_error_appears_on_page(expected_error=expected_error)



