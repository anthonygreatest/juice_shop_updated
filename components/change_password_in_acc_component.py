from components.base_component import BaseComponent
from data.locators.change_password_locators import ChangePasswordLocators
from elements.input import Input


class ChangePassInAccComponent(BaseComponent):

    def __init__(self, page):
        super().__init__(page)
        self.locators = ChangePasswordLocators
        self.current_password_input = Input(page, self.locators.current_password, 'Current Password')
        self.new_password_input = Input(page, self.locators.new_password, 'New Password')
        self.password_repeat_input = Input(page, self.locators.password_repeat, 'Password Repeat')
        self.fields = {
            'current': self.current_password_input,
            'new': self.new_password_input,
            'repeat': self.password_repeat_input
        }

    def fill(self, **data):

        if data.get('current'):
            self.current_password_input.fill(str(data.get('current')))
            self.current_password_input.check_have_value(data.get('current'))
        if data.get('new'):
            self.new_password_input.fill(str(data.get('new')))
            self.new_password_input.check_have_value(data.get('new'))
        if data.get('repeat'):
            self.password_repeat_input.fill(str(data.get('repeat')))
            self.password_repeat_input.check_have_value(data.get('repeat'))

    def leave_field_empty(self, field):
        empty_field = self.fields[field]
        empty_field.fill('')
        empty_field.blur()

    def check_visible(self, current_password, new_password, repeat_password):
        self.current_password_input.check_visible()
        self.current_password_input.check_have_value(current_password)

        self.new_password_input.check_visible()
        self.new_password_input.check_have_value(new_password)

        self.password_repeat_input.check_visible()
        self.password_repeat_input.check_have_value(repeat_password)
