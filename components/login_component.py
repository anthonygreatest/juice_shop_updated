from playwright.sync_api import Page

from components.base_component import BaseComponent
from data.locators.login_page_locators import LoginLocators
from elements.input import Input


class LoginComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = LoginLocators

        self.email_input = Input(page, self.locators.email, 'Email')
        self.password_input = Input(page, self.locators.password, 'Password')
        self.fields = {
            'email': self.email_input,
            'password': self.password_input
        }

    def fill(self, **data):

        if data.get('email'):
            self.email_input.fill(str(data.get('email', '')))
            self.email_input.check_have_value(data.get('email'))

        if data.get('password'):
            self.password_input.fill(str(data.get('password', '')))
            self.password_input.check_have_value(data.get('password'))

        if data.get('new'):
            self.password_input.fill(str(data.get('new', '')))
            self.password_input.check_have_value(data.get('new'))

    def leave_fields_empty(self, field):
        empty_field = self.fields.get(field)
        empty_field.click()
        empty_field.blur()

    def check_visible(self, email, password):
        self.email_input.check_visible()
        self.email_input.check_have_value(email)

        self.password_input.check_visible()
        self.password_input.check_have_value(password)