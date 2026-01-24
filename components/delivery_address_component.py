from playwright.sync_api import Page

from components.base_component import BaseComponent
from data.locators.delivery_page_locators import DeliveryPageLocators
from elements.text import Text


class DeliveryAddressComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = DeliveryPageLocators
        self.delivery_info = Text(page, self.locators.delivery_info, 'Delivery Info')
