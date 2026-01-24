from playwright.sync_api import Page

from components.base_component import BaseComponent
from data.locators.payment_options_page_locators import PaymentOptionsPageLocators
from elements.button import Button
from elements.dropdown import Dropdown
from elements.input import Input


class CardFormComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = PaymentOptionsPageLocators
        self.open_card_form_btn = Button(page, self.locators.open_card_form, 'Open card form')
        self.name_input = Input(page, self.locators.name, 'Name')
        self.card_num_input = Input(page, self.locators.card_number, 'Card Number')
        self.expiry_month = Dropdown(page, self.locators.expiry_month, 'Expiry Month')
        self.expiry_year = Dropdown(page, self.locators.expiry_year, 'Expiry Year')
        self.submit_btn = Button(page, self.locators.submit_btn, 'Submit')
        self.select_card_btn = Button(page, self.locators.select_card_radio_btn, 'Select card')
        self.fields = {
            'full_name': self.name_input,
            'card_num': self.card_num_input,
            'exp_month': self.expiry_month,
            'exp_year': self.expiry_year
        }

    def click_submit(self):
        self.submit_btn.check_enabled()
        self.submit_btn.click()

    def select_card(self):
        self.select_card_btn.check_enabled()
        self.select_card_btn.click()

    def open_card_form(self):
        self.open_card_form_btn.check_enabled()
        self.open_card_form_btn.click()

    def fill(self, **data):
        self.open_card_form()

        if data.get('full_name'):
            self.name_input.fill(str(data.get('full_name', '')))
            self.name_input.check_have_value(str(data.get('full_name', '')))

        if data.get('card_num'):
            self.card_num_input.fill(str(data.get('card_num', '')))
            self.card_num_input.check_have_value(str(data.get('card_num', '')))

        if data.get('exp_month'):
            self.expiry_month.select_option_in_dropdown(str(data.get('exp_month', '')))
            # self.expiry_month.check_have_text(str(data.get('expMonth', '')))

        if data.get('exp_year'):
            self.expiry_year.select_option_in_dropdown(str(data.get('exp_year', '')))
            # self.expiry_year.check_have_text(str(data.get('expYear', '')))

    def leave_fields_empty(self, field):
        empty_field = self.fields[field]
        empty_field.click()
        self.page.mouse.click(1, 1)


    def check_visible(self, card_num, name, expiry_year, expiry_month):

        self.name_input.check_visible()
        self.name_input.check_have_value(name)

        self.card_num_input.check_visible()
        self.card_num_input.check_have_value(card_num)

        self.expiry_year.check_visible()
        self.expiry_year.check_contain_text(expiry_year)

        self.expiry_month.check_visible()
        self.expiry_month.check_contain_text(expiry_month)
