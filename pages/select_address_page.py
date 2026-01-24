from components.saved_address_component import SavedAddressComponent
from components.toast_component import ToastComponent
from data.locators.select_address_page_locators import SelectAddressPageLocators
from elements.button import Button
from pages.base_page import BasePage
from pages.mixins import NegativeTestsMixin


class SelectAddressPage(BasePage, NegativeTestsMixin):

    ADDRESS_ADDED_TOAST = lambda self, city: f'The address at {city} has been successfully added to your addresses.'

    def __init__(self, page):
        super().__init__(page)
        self.locators = SelectAddressPageLocators()
        self.add_address_btn = Button(page, self.locators.add_new_address_btn, 'Add new address Button')
        self.saved_address_component = SavedAddressComponent(page)
        self.toast = ToastComponent(page)
        self.continue_btn = Button(page, self.locators.continue_btn, 'Continue Button')

    def click_add_new_address(self):
        self.add_address_btn.check_enabled()
        self.add_address_btn.click()

    def select_address_and_continue(self):
        self.saved_address_component.click_select_address()
        self.continue_btn.check_enabled()
        self.continue_btn.click()

    #до недавнего времени было чз expected_data: пайдентик схема
    def check_address_matches_expected(self, expected_data: dict):
        self.saved_address_component.address_info.check_contain_text(expected_data["street_address"], nth=2)
        self.saved_address_component.address_info.check_contain_text(expected_data["zip_code"], nth=2)
        self.saved_address_component.address_info.check_contain_text(expected_data["city"], nth=2)
        self.saved_address_component.address_info.check_have_text(expected_data["full_name"], nth=1)
        self.saved_address_component.address_info.check_have_text(expected_data["country"], nth=3)

        if expected_data.get('state'):
            self.saved_address_component.address_info.check_contain_text(expected_data['state'], nth=2)

    def check_address_added_toast_appears_on_page(self, city):
        self.toast.check_toast_text(self.ADDRESS_ADDED_TOAST(city))

    def check_continue_to_delivery_button_remains_disabled(self):
        self.continue_btn.check_disabled()