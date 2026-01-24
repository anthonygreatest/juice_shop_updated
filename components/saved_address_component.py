from playwright.sync_api import Page

from components.base_component import BaseComponent
from components.toast_component import ToastComponent
from data.locators.select_address_page_locators import SelectAddressPageLocators
from elements.button import Button
from elements.text import Text


class SavedAddressComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = SelectAddressPageLocators
        self.address_info = Text(page, self.locators.created_address, 'Address Info')
        self.select_address_btn = Button(page, self.locators.select_address_radio_btn, 'Select address')

    def click_select_address(self):
        self.select_address_btn.check_enabled()
        self.select_address_btn.click()

