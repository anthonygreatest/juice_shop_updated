from components.base_component import BaseComponent
from data.locators.change_password_locators import ChangePasswordLocators
from elements.input import Input


class ChangePasswordComponent(BaseComponent):

    def __init__(self, page):
        super().__init__(page)
        self.locators = ChangePasswordLocators
        self.email_input = Input(page, self.locators.email, 'Email')
        self.security_question_input = Input(page, self.locators.security_question, 'Security Question')
        self.new_password_input = Input(page, self.locators.new_password, 'New Password')
        self.repeat_password_input = Input(page, self.locators.password_repeat, 'Repeat New Password')
        self.current_password_input = Input(page, self.locators.current_password, 'Current Password')
        self.fields = {
            'email': self.email_input,
            'answer': self.security_question_input,
            'new': self.new_password_input,
            'repeat': self.repeat_password_input
        }

    def fill(self, **data):

        if data.get('email'):
            self.email_input.fill(str(data.get('email', '')))
            self.email_input.check_have_value(data.get('email'))

        if data.get('answer'):
            self.security_question_input.fill(str(data.get('answer', '')))
            self.security_question_input.check_have_value(data.get('answer'))

        if data.get('new'):
            self.new_password_input.fill(str(data.get('new', '')))
            self.new_password_input.check_have_value(data.get('new'))

        if data.get('repeat'):
            self.repeat_password_input.fill(str(data.get('repeat', '')))
            self.repeat_password_input.check_have_value(data.get('repeat'))

    def leave_field_empty(self, field):
        empty_field = self.fields[field]
        empty_field.fill('')
        empty_field.blur()

    def check_visible(self, email, password, new_password, repeat_password):
        self.email_input.check_visible()
        self.email_input.check_have_value(email)

        self.security_question_input.check_visible()
        self.security_question_input.check_have_value(password)

        self.new_password_input.check_visible()
        self.new_password_input.check_have_value(new_password)

        self.repeat_password_input.check_visible()
        self.repeat_password_input.check_have_value(repeat_password)
