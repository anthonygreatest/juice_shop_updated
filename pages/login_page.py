from components.login_component import LoginComponent
from components.toast_component import ToastComponent
from data.locators.login_page_locators import LoginLocators
from elements.button import Button
from elements.link import Link
from elements.text import Text
from pages.base_page import BasePage
from pages.mixins import NegativeTestsMixin, DismissBannerMixin


class LoginPage(BasePage, NegativeTestsMixin, DismissBannerMixin):

    SUCCESS_REGISTER_TEXT = 'Registration completed successfully. You can now log in.'
    INVALID_ENTRY_DATA = 'Invalid email or password.'
    EMPTY_EMAIL = 'Please provide an email address.'
    EMPTY_PASSWORD = 'Please provide a password.'

    def __init__(self, page):
        super().__init__(page)
        self.locators = LoginLocators()
        self.toast = ToastComponent(page)
        self.login_form = LoginComponent(page)
        self.login_button = Button(page, self.locators.login_btn, 'Login Button')
        self.forgot_password_link = Link(page, self.locators.forgot_your_password_link, 'Forgot your password Link')
        self.register_link = Link(page, self.locators.register_link, 'Not yet a customer Link')
        self.form_error = Text(page, self.FORM_ERROR, 'Form error')
        self.field_error = Text(page, self.ERROR, 'Field error')

    def open(self, url: str):
        super().open(url)
        self.close_welcome_banner()

    def click_login_btn(self):
        self.login_button.click()
        # self.check_current_url('/#/search')

    def click_forgot_password(self):
        self.forgot_password_link.click()
        self.check_current_url('*/forgot-password')

    def click_register(self):
        self.register_link.click()
        self.check_current_url('*/register')

    def check_user_registered_toast_appears_on_page(self):
        self.toast.check_toast_text(self.SUCCESS_REGISTER_TEXT)

    def check_invalid_data_error_appears_on_page(self):
        self.form_error.check_contain_text(self.INVALID_ENTRY_DATA)

    def check_empty_field_error_appears_on_page(self, expected_error):
        self.field_error.check_have_text(expected_error)

    def check_login_button_remains_disabled(self):
        self.login_button.check_disabled()
