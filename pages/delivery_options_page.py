from components.delivery_address_component import DeliveryAddressComponent
from data.locators.delivery_page_locators import DeliveryPageLocators
from elements.button import Button
from pages.base_page import BasePage
from pages.mixins import NegativeTestsMixin
from utils.schemas.add_address_request_schema import AddAddressSchema


class DeliveryOptionsPage(BasePage, NegativeTestsMixin):

    def __init__(self, page):
        super().__init__(page)
        self.locators = DeliveryPageLocators()
        self.delivery_address_component = DeliveryAddressComponent(page)
        self.delivery_option_btn = Button(page, self.locators.delivery_option, 'Delivery option Button')
        self.continue_btn = Button(page, self.locators.continue_to_payment, 'Continue Button')

    def check_delivery_info_matches_expected(self, delivery_data: AddAddressSchema):
        self.delivery_address_component.delivery_info.check_have_text(delivery_data.full_name, nth=0)
        self.delivery_address_component.delivery_info.check_contain_text(delivery_data.street_address, nth=1)
        self.delivery_address_component.delivery_info.check_contain_text(delivery_data.zip_code, nth=1)
        self.delivery_address_component.delivery_info.check_contain_text(delivery_data.city, nth=1)
        self.delivery_address_component.delivery_info.check_have_text(delivery_data.country, nth=2)
        self.delivery_address_component.delivery_info.check_contain_text(str(delivery_data.mobile_num), nth=3)

        if delivery_data.state is not None:
            self.delivery_address_component.delivery_info.check_contain_text(delivery_data.state, nth=1)

    def select_delivery_option_and_continue(self, days):
        if days == 1:
            self.delivery_option_btn.click(nth=0)
        if days == 3:
            self.delivery_option_btn.click(nth=1)
        if days == 5:
            self.delivery_option_btn.click(nth=2)
        self.click_continue()

    def click_continue(self):
        self.continue_btn.check_enabled()
        self.continue_btn.click()

    def check_continue_to_payment_button_remains_disabled(self):
        self.continue_btn.check_disabled()
