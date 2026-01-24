from components.address_form_component import AddressFormComponent
from data.locators.address_page_locators import AddressPageLocators
from elements.button import Button
from elements.text import Text
from pages.base_page import BasePage
from pages.mixins import NegativeTestsMixin


class AddressPage(BasePage, NegativeTestsMixin):

    EMPTY_COUNTRY = 'Please provide a country.'
    EMPTY_CITY = 'Please provide a city.'
    EMPTY_ZIP_CODE = 'Please provide a ZIP code.'
    EMPTY_MOBILE_NUM = 'Please provide a mobile number.'
    EMPTY_NAME = 'Please provide a name.'
    EMPTY_ADDRESS = 'Please provide an address.'
    INVALID_MOBILE_NUM = 'Mobile number must match {{range}} format.'

    def __init__(self, page):
        super().__init__(page)
        self.locators = AddressPageLocators()
        self.address_form = AddressFormComponent(page)
        self.submit_btn = Button(page, self.locators.submit_btn, 'Submit Button')
        self.field_error = Text(page, self.ERROR, 'Field error')

    def click_submit(self):
        self.submit_btn.check_enabled()
        self.submit_btn.scroll_into_view_if_needed()
        self.submit_btn.click()

    def check_empty_field_error_appears_on_page(self, expected_error):
        self.field_error.check_contain_text(expected_error)

    def check_submit_button_remains_disabled(self):
        self.submit_btn.scroll_into_view_if_needed()
        self.submit_btn.check_disabled()

    def check_invalid_mobile_num_error_appears_on_page(self):
        self.field_error.check_contain_text(self.INVALID_MOBILE_NUM)

    def check_field_value_not_valid(self, field):
        field = self.address_form.fields[field]
        field.check_have_attribute(attribute='aria-invalid', value='true')