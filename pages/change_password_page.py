from components.change_password_component import ChangePasswordComponent
from components.change_password_in_acc_component import ChangePassInAccComponent
from components.navbar_component import NavbarMenuComponent
from data.locators.change_password_locators import ChangePasswordLocators
from elements.button import Button
from elements.text import Text
from pages.base_page import BasePage
from pages.mixins import LogoutMixin, NegativeTestsMixin


class ChangePasswordPage(BasePage, LogoutMixin, NegativeTestsMixin):

    CONFIRMATION_TEXT = 'Your password was successfully changed.'
    EMPTY_EMAIL = 'Please provide an email address.'
    INVALID_EMAIL = 'Email address is not valid.'
    EMPTY_SECURITY_QUESTION = 'Please provide an answer to your security question.'
    EMPTY_NEW_PASSWORD = 'Please provide your new password.'
    EMPTY_REPEAT_NEW_PASSWORD = 'Please repeat your password.'
    PASSWORD_MISMATCH = 'Passwords do not match'
    SECURITY_ANSWER_ERROR = 'Wrong answer to security question.'
    CURRENT_PASSWORD_ERROR = 'Current password is not correct.'
    EMPTY_CURRENT_PASSWORD = 'Please provide your current password.'
    PASSWORD_LENGTH_ERROR = 'Password must be {{length}} characters long.'


    def __init__(self, page):
        super().__init__(page)
        self.locators = ChangePasswordLocators()
        self.change_password_form = ChangePasswordComponent(page)
        self.reset_password_button = Button(page, self.locators.reset_btn, 'Change password')
        self.change_password_btn = Button(page, self.locators.change_password_btn, 'Change password')
        self.change_pass_in_acc_form = ChangePassInAccComponent(page)
        self.confirmation_text = Text(page, self.locators.confirmation, 'Confirmation text')
        self.navbar = NavbarMenuComponent(page)
        self.field_error = Text(page, self.ERROR, 'Field error')
        self.form_error = Text(page,self.locators.form_error, 'Form error')

    def open(self, url: str):
        super().open(url)
        self.close_welcome_banner()

    def click_reset_password(self):
        self.reset_password_button.check_enabled()
        self.reset_password_button.click()
        self.check_current_url('/#/forgot-password')

    def reset_password(self, **data):
        self.change_password_form.fill(
            **data
        )
        self.click_reset_password()

    def change_password_after_login(self, **data):
        self.change_pass_in_acc_form.fill(**data)
        self.click_change_password()

    def click_change_password(self):
        self.change_password_btn.check_enabled()
        self.change_password_btn.click()

    def check_password_changed_confirmation_appears_on_page(self):
        self.confirmation_text.check_contain_text(self.CONFIRMATION_TEXT)

    def check_reset_password_button_remains_disabled(self):
        self.reset_password_button.check_disabled()

    def check_change_password_button_remains_disabled(self):
        self.change_password_btn.check_disabled()

    def check_fields_remain_disabled(self):
        attribute = 'disabled'
        self.change_password_form.security_question_input.check_attribute_exists(attribute=attribute)
        self.change_password_form.new_password_input.check_attribute_exists(attribute=attribute)
        self.change_password_form.repeat_password_input.check_attribute_exists(attribute=attribute)

    def check_empty_field_error_appears_on_page(self, expected_error):
        self.field_error.check_contain_text(expected_error)

    def check_invalid_field_error_appears_on_page(self, expected_error):
        self.field_error.check_contain_text(expected_error)

    def check_wrong_security_answer_error_appears_on_page(self):
        self.form_error.check_contain_text(self.SECURITY_ANSWER_ERROR)

    def check_field_value_not_valid(self, field):
        field = self.change_password_form.fields[field]
        field.check_have_attribute(attribute='aria-invalid', value='true')

    def check_current_password_error_appears_on_page(self):
        self.form_error.check_contain_text(self.CURRENT_PASSWORD_ERROR)

