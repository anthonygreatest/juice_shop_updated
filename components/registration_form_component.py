from playwright.sync_api import Page

from components.base_component import BaseComponent
from data.locators.register_page_locators import RegisterPageLocators
from elements.dropdown import Dropdown
from elements.input import Input


class RegistrationFormComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = RegisterPageLocators

        self.email_input = Input(page, self.locators.email, 'Email')
        self.password_input = Input(page, self.locators.password, 'Password')
        self.security_question_dropdown = Dropdown(page, self.locators.security_question_dropdown, 'Security Question')
        self.repeat_password_input = Input(page, self.locators.password_repeat, 'Repeat Password')
        self.answer_input = Input(page, self.locators.security_answer, 'Answer')
        self.fields = {
            'email': self.email_input,
            'password': self.password_input,
            'password_repeat': self.repeat_password_input,
            'security_question': self.security_question_dropdown,
            'security_answer': self.answer_input
        }

    def fill(self, **data):

        if data.get('email'):
            self.email_input.fill(str(data.get('email', '')))
            self.email_input.check_have_value(str(data.get('email', '')))

        if data.get('password'):
            self.password_input.fill(str(data.get('password', '')))
            self.password_input.check_have_value(str(data.get('password', '')))

        if data.get('password_repeat'):
            self.repeat_password_input.fill(str(data.get('password_repeat', '')))
            self.repeat_password_input.check_have_value(str(data.get('password_repeat', '')))

        if data.get('security_question'):
            self.security_question_dropdown.choose_option(str(data.get('security_question', '')))
            self.security_question_dropdown.check_have_text(str(data.get('security_question', '')))

        if data.get('security_answer'):
            self.answer_input.fill(str(data.get('security_answer', '')))
            self.answer_input.check_have_value(str(data.get('security_answer', '')))

    def leave_field_empty(self, field):
        field_to_blur = self.fields.get(field)
        field_to_blur.click()
        self.page.mouse.click(1, 1)

    def check_visible(self, email, password, repeat_password, security_question, answer):

        self.email_input.check_visible()
        self.email_input.check_have_value(email)

        self.password_input.check_visible()
        self.password_input.check_have_value(password)

        self.security_question_dropdown.check_visible()
        self.security_question_dropdown.check_have_text(security_question)

        self.repeat_password_input.check_visible()
        self.repeat_password_input.check_have_value(repeat_password)

        self.answer_input.check_visible()
        self.answer_input.check_have_value(answer)