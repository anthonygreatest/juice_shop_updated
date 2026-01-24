import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from pages.change_password_page import ChangePasswordPage
from utils.helper import prepare_register_payload, change_password_payload, \
    create_invalid_fields


@pytest.mark.screenshot
@allure.feature('Change Password')
@allure.story('Invalid forgot your password flow')
class TestForgotYourPasswordNegative:

    @allure.title('Unregistered user not able to change password')
    def test_not_registered_user_not_able_to_change_password(self, forgot_your_password_page):

        new_data = {
            'email': prepare_register_payload().email
        }

        forgot_your_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD)
        forgot_your_password_page.change_password_form.fill(
            **new_data
        )

        forgot_your_password_page.check_reset_password_button_remains_disabled()
        forgot_your_password_page.check_fields_remain_disabled()

    @allure.title('User not able to change password without email')
    def test_change_password_without_email(self, forgot_your_password_page):

        forgot_your_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD)

        forgot_your_password_page.change_password_form.leave_field_empty('email')

        forgot_your_password_page.check_reset_password_button_remains_disabled()
        forgot_your_password_page.check_fields_remain_disabled()
        forgot_your_password_page.check_empty_field_error_appears_on_page(
            forgot_your_password_page.EMPTY_EMAIL
        )


    @allure.title('User not able to change password with invalid email')
    def test_change_password_invalid_email(self, forgot_your_password_page):

        forgot_your_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD)

        new_data = {
            'email': '12345'
        }

        forgot_your_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD)
        forgot_your_password_page.change_password_form.fill(
            **new_data
        )

        forgot_your_password_page.change_password_form.email_input.blur()

        forgot_your_password_page.check_reset_password_button_remains_disabled()
        forgot_your_password_page.check_fields_remain_disabled()
        forgot_your_password_page.check_invalid_field_error_appears_on_page(
            forgot_your_password_page.INVALID_EMAIL
        )

    @allure.title('User not able to change password with wrong security answer')
    def test_change_password_wrong_security_answer(self, forgot_your_password_page, register):

        forgot_your_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD)

        new_data = change_password_payload(register)
        new_data['answer'] = '12345'

        forgot_your_password_page.reset_password(
            **new_data
        )

        forgot_your_password_page.check_wrong_security_answer_error_appears_on_page()

    @pytest.mark.parametrize('missing_field, expected_error', [
        ('answer', ChangePasswordPage.EMPTY_SECURITY_QUESTION),
        ('new', ChangePasswordPage.EMPTY_NEW_PASSWORD),
        ('repeat', ChangePasswordPage.EMPTY_REPEAT_NEW_PASSWORD)
    ])
    @allure.title('User not able to change password with invalid and missing data')
    def test_change_password_with_missing_data(self, forgot_your_password_page, missing_field, expected_error, register):

        new_data = change_password_payload(register)
        new_data.pop(missing_field)

        forgot_your_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD)
        forgot_your_password_page.reload()

        forgot_your_password_page.change_password_form.fill(
            **new_data
        )

        forgot_your_password_page.change_password_form.leave_field_empty(missing_field)

        forgot_your_password_page.check_reset_password_button_remains_disabled()
        forgot_your_password_page.check_empty_field_error_appears_on_page(expected_error=expected_error)


    @allure.title('User not able to change password with invalid and missing data')
    def test_change_password_with_invalid_password_data(self, forgot_your_password_page,register):

        new_data = change_password_payload(register)
        invalid_password_data = create_invalid_fields(
            invalid_fields=[('new', '1234'), ('repeat', '12345')],
            data=new_data
        )

        forgot_your_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD)
        forgot_your_password_page.reload()

        forgot_your_password_page.change_password_form.fill(
            **invalid_password_data
        )

        forgot_your_password_page.change_password_form.repeat_password_input.blur()

        forgot_your_password_page.check_reset_password_button_remains_disabled()
        forgot_your_password_page.check_invalid_field_error_appears_on_page(
            expected_error=ChangePasswordPage.PASSWORD_MISMATCH
        )
        forgot_your_password_page.check_field_value_not_valid('new')


@allure.feature('Change Password')
@allure.story('Invalid change your password after login flow')
class TestChangePasswordAfterLoginNegative:

    @allure.title('User not able to change password while logged in using wrong password')
    def test_change_password_while_logged_in_using_wrong_current_password(self, change_password_after_login_page):

        change_password_page, new_user_data = change_password_after_login_page

        new_user_data['current'] = '12345'

        change_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD_IN_ACCOUNT)
        change_password_page.change_password_after_login(
            **new_user_data
        )

        change_password_page.check_current_password_error_appears_on_page()

    @pytest.mark.parametrize('missing_field, expected_error', [
        ('current', ChangePasswordPage.EMPTY_CURRENT_PASSWORD),
        ('new', ChangePasswordPage.EMPTY_NEW_PASSWORD),
        ('repeat', ChangePasswordPage.EMPTY_REPEAT_NEW_PASSWORD)
    ])
    @allure.title('User not able to change password while logged in using empty fields')
    def test_change_password_while_logged_in_with_empty_fields(self, change_password_after_login_page, missing_field, expected_error):

        change_password_page, new_user_data = change_password_after_login_page
        new_user_data.pop(missing_field)

        change_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD_IN_ACCOUNT)
        change_password_page.change_pass_in_acc_form.fill(
            **new_user_data
        )

        change_password_page.change_pass_in_acc_form.leave_field_empty(missing_field)

        change_password_page.check_empty_field_error_appears_on_page(expected_error)
        change_password_page.check_change_password_button_remains_disabled()

    @pytest.mark.parametrize('field, value, expected_error', [
        ('new', 'a' * 41, ChangePasswordPage.PASSWORD_LENGTH_ERROR),
        ('repeat', 'a' * 5, ChangePasswordPage.PASSWORD_MISMATCH)
    ])
    @allure.title('User not able to change password while logged in using invalid data')
    def test_change_password_while_logged_in_with_invalid_data(self, change_password_after_login_page, field, value,
        expected_error):

        change_password_page, new_user_data = change_password_after_login_page

        new_user_data[field] = value

        change_password_page.open(PlaywrightEndpoints.CHANGE_PASSWORD_IN_ACCOUNT)
        change_password_page.change_pass_in_acc_form.fill(
            **new_user_data
        )

        change_password_page.change_pass_in_acc_form.password_repeat_input.blur()

        change_password_page.check_invalid_field_error_appears_on_page(expected_error=expected_error)
        change_password_page.check_change_password_button_remains_disabled()
