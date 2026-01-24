from components.address_form_component import AddressFormComponent
from components.saved_address_component import SavedAddressComponent
from components.toast_component import ToastComponent
from data.frontend_endpoints import PlaywrightEndpoints
from data.locators.address_page_locators import AddressPageLocators
from elements.button import Button
from pages.base_page import BasePage
from utils.schemas.add_address_request_schema import AddAddressSchema


class SavedAddressesPage(BasePage):

    ADDRESS_EDITED_TOAST = lambda self, city: f'The address at {city} has been successfully updated.'

    def __init__(self, page):
        super().__init__(page)
        self.locators = AddressPageLocators()
        self.saved_address_component = SavedAddressComponent(page)
        self.edit_btn = Button(page, self.locators.edit_btn, 'Edit Address Button')
        self.remove_btn = Button(page, self.locators.delete_address_btn, 'Remove Address Button')
        self.address_form = AddressFormComponent(page)
        self.submit_btn = Button(page, self.locators.submit_btn, 'Submit address Button')
        self.address_update_toast = ToastComponent(page)

    def check_address_data_on_saved_addresses_page_matches_expected(self, expected_data: dict):
        self.saved_address_component.address_info.check_contain_text(expected_data["street_address"], nth=1, specified_name=' (street_address)')
        self.saved_address_component.address_info.check_contain_text(expected_data["zip_code"], nth=1, specified_name=' (zip_code)')
        self.saved_address_component.address_info.check_contain_text(expected_data["city"], nth=1, specified_name=' (city)')
        self.saved_address_component.address_info.check_have_text(expected_data["full_name"], nth=0, specified_name=' (full_name)')
        self.saved_address_component.address_info.check_have_text(expected_data["country"], nth=2, specified_name=' (country)')

        if expected_data.get('state'):
            self.saved_address_component.address_info.check_contain_text(expected_data['state'], nth=1, specified_name=' (state)')

    def remove_address(self):
        self.remove_btn.check_enabled()
        self.remove_btn.click()

    def edit_address(self):
        self.edit_btn.check_enabled()
        self.edit_btn.click()

    def get_num_of_addresses_on_page(self):
        return self.saved_address_component.address_info.count_elements()

    def click_submit(self):
        self.submit_btn.check_enabled()
        self.submit_btn.click()

    def check_address_updated_toast_appears_on_page(self, city):
        self.address_update_toast.check_toast_text(self.ADDRESS_EDITED_TOAST(city))
