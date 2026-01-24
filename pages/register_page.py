import re

from components.registration_form_component import RegistrationFormComponent
from data.frontend_endpoints import PlaywrightEndpoints
from data.locators.register_page_locators import RegisterPageLocators
from elements.button import Button
from elements.text import Text
from pages.base_page import BasePage
from pages.login_page import LoginPage, DismissBannerMixin
from pages.mixins import NegativeTestsMixin


class RegisterPage(BasePage, NegativeTestsMixin, DismissBannerMixin):

    EMAIL_NOT_VALID = 'Email address is not valid.'
    EMPTY_EMAIL = 'Please provide an email address.'
    EMPTY_PASSWORD = 'Please provide a password.'
    PASSWORD_WRONG_LENGTH = 'Password must be 5-40 characters long.'
    PASSWORD_MISMATCH = 'Passwords do not match'
    REPEAT_PASSWORD_EMPTY = 'Please repeat your password.'
    SECURITY_ANSWER_EMPTY = 'Please provide an answer to your security question.'
    SECURITY_QUESTION_EMPTY = 'Please select a security question.'
    EMAIL_NOT_UNIQUE = 'Email must be unique'

    def __init__(self, page):
        super().__init__(page)
        self.locators = RegisterPageLocators()
        self.registration_form = RegistrationFormComponent(page)
        self.register_button = Button(page, self.locators.register_btn, 'Register Button')
        self.form_error = Text(page, self.FORM_ERROR, 'Form error')
        self.field_error = Text(page, self.ERROR, 'Field error')

    def open(self, url: str):
        super().open(url)
        self.close_welcome_banner()

    def click_register_button(self):
        self.register_button.click()
        # self.check_current_url(re.compile(".*/login"))

    def register(self, **data):
        self.registration_form.fill(**data)
        self.click_register_button()

    def check_email_not_unique_error_appears_on_page(self):
        self.form_error.check_contain_text(self.EMAIL_NOT_UNIQUE)

    def check_register_button_remains_disabled(self):
        self.register_button.check_disabled()

    def check_empty_field_error_appears_on_page(self, expected_error):
        self.field_error.check_have_text(expected_error)

    def check_invalid_field_error_appears_on_page(self, expected_error):
        self.field_error.check_have_text(expected_error)
