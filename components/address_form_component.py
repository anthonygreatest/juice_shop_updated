from playwright.sync_api import Page

from components.base_component import BaseComponent
from data.locators.address_page_locators import AddressPageLocators
from elements.input import Input


class AddressFormComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = AddressPageLocators

        self.country_input = Input(page, self.locators.country, 'Country')
        self.name_input = Input(page, self.locators.name, 'Name')
        self.mobile_num_input = Input(page, self.locators.mobile_number, 'Mobile Number')
        self.zip_code_input = Input(page, self.locators.zip_code, 'Zip Code')
        self.street_address_input = Input(page, self.locators.address, 'Street Address')
        self.city_input = Input(page, self.locators.city, 'City')
        self.state_input = Input(page, self.locators.state, 'State')
        self.fields = {
            'country': self.country_input,
            'full_name': self.name_input,
            'mobile_num': self.mobile_num_input,
            'zip_code': self.zip_code_input,
            'street_address': self.street_address_input,
            'city': self.city_input,
            'state': self.state_input
        }

    def fill(self, **data):

        if data.get('country'):
            self.country_input.fill(str(data.get('country', '')))
            self.country_input.check_have_value(str(data.get('country', '')))

        if data.get('full_name'):
            self.name_input.fill(str(data.get('full_name', '')))
            self.name_input.check_have_value(str(data.get('full_name', '')))

        if data.get('mobile_num'):
            self.mobile_num_input.fill(str(data.get('mobile_num', '')))
            self.mobile_num_input.check_have_value(str(data.get('mobile_num', '')))

        if data.get('zip_code'):
            self.zip_code_input.fill(str(data.get('zip_code', '')))
            self.zip_code_input.check_have_value(str(data.get('zip_code', '')))

        if data.get('street_address'):
            self.street_address_input.fill(str(data.get('street_address', '')))
            self.street_address_input.check_have_value(str(data.get('street_address', '')))

        if data.get('city'):
            self.city_input.fill(str(data.get('city', '')))
            self.city_input.check_have_value(str(data.get('city', '')))

        if data.get('state'):
            self.state_input.fill(str(data.get('state', '')))
            self.state_input.check_have_value(str(data.get('state', '')))

    def leave_field_empty(self, field):
        field_to_blur = self.fields.get(field)
        field_to_blur.click()
        field_to_blur.blur()

    def check_visible(self, country, name, mobile_num, zip_code, street_address, city, state):

        self.country_input.check_visible()
        self.country_input.check_have_value(country)

        self.name_input.check_visible()
        self.name_input.check_have_value(name)

        self.mobile_num_input.check_visible()
        self.mobile_num_input.check_have_text(mobile_num)

        self.zip_code_input.check_visible()
        self.zip_code_input.check_have_value(zip_code)

        self.street_address_input.check_visible()
        self.street_address_input.check_have_value(street_address)

        self.city_input.check_visible()
        self.city_input.check_have_value(city)

        self.state_input.check_visible()
        self.state_input.check_have_value(state)