import json
import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from pages.register_page import RegisterPage
from tests.tests_frontend.frontend_helpers import formatted_register_payload_for_ui
from utils.helper import register_user_and_set_security_answer


@pytest.mark.screenshot
@allure.feature('User Registration')
@allure.story('Invalid registration flow')
class TestRegisterPageNegative:

    @allure.title('User not registered with invalid or missing data')
    @pytest.mark.parametrize('missing_field, expected_error', [
        ('email', RegisterPage.EMPTY_EMAIL),
        ('password', RegisterPage.EMPTY_PASSWORD),
        ('password_repeat', RegisterPage.REPEAT_PASSWORD_EMPTY),
        ('security_question', RegisterPage.SECURITY_QUESTION_EMPTY),
        ('security_answer', RegisterPage.SECURITY_ANSWER_EMPTY)
    ])
    def test_register_user_with_missing_data(self, register_page,
        missing_field, expected_error):

        invalid_payload = formatted_register_payload_for_ui()
        invalid_payload.pop(missing_field)

        register_page.open(PlaywrightEndpoints.REGISTER)
        register_page.registration_form.fill(
            **invalid_payload
        )
        register_page.registration_form.leave_field_empty(missing_field)

        register_page.check_register_button_remains_disabled()
        register_page.check_empty_field_error_appears_on_page(expected_error=expected_error)

    @allure.title('User not registered with invalid or missing data')
    @pytest.mark.parametrize('invalid_field, value, expected_error', [
        ('email', '@!walter', RegisterPage.EMAIL_NOT_VALID),
        ('password', 1, RegisterPage.PASSWORD_WRONG_LENGTH),
        ('password', 'a' * 41, RegisterPage.PASSWORD_WRONG_LENGTH),
        ('password_repeat', 123, RegisterPage.PASSWORD_MISMATCH)
    ])
    @allure.title('User not registered without security question and answer')
    def test_register_user_with_invalid_data(self, register_page, invalid_field, value, expected_error):

        invalid_payload = formatted_register_payload_for_ui()
        invalid_payload[invalid_field] = value

        register_page.open(PlaywrightEndpoints.REGISTER)
        register_page.registration_form.fill(
            **invalid_payload
        )

        register_page.check_register_button_remains_disabled()
        register_page.check_invalid_field_error_appears_on_page(expected_error=expected_error)

    @allure.title('Same user not registered second time')
    def test_register_same_user_second_time(self, register_page, register):

        validated_response, registered_user = register_user_and_set_security_answer(register)
        formatted_data = registered_user.model_dump()
        formatted_data['security_question'] = registered_user.security_question.question

        register_page.open(PlaywrightEndpoints.REGISTER)
        register_page.register(
            **formatted_data
        )

        register_page.check_email_not_unique_error_appears_on_page()


