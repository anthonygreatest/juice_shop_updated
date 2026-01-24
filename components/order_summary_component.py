from playwright.sync_api import Page

from components.base_component import BaseComponent
from data.locators.checkout_page_locators import CheckoutPageLocators
from elements.text import Text


class OrderSummaryComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = CheckoutPageLocators
        self.order_summary_data = Text(page, self.locators.order_summary_data, 'Order summary data')