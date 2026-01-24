from decimal import Decimal
from components.basket_component import BasketComponent
from data.dataclasses.selected_product_data import SelectedProductData
from data.locators.completion_page_locators import CompletionPageLocators
from elements.button import Button
from elements.link import Link
from elements.text import Text
from pages.base_page import BasePage
from pages.mixins import LinkAccessMixin
from utils.schemas.add_address_resp_schema import AddAddressRespSchema
from utils.schemas.delivery_options_resp_schema import DeliveryOptionsRespSchema


class CompletionPage(BasePage, LinkAccessMixin):

    EXPECTED_THANKS_TEXT = 'Thank you for your purchase!'
    TWITTER_REPOST_LINK = lambda self, purchase: f'https://twitter.com/intent/tweet?text=I just purchased%0a- {purchase}%0afrom @owasp_juiceshop&hashtags=security'

    def __init__(self, page):
        super().__init__(page)
        self.locators = CompletionPageLocators()
        self.thanks_text = Text(page, self.locators.thanks_locator, 'Thanks for order Text')
        self.basket = BasketComponent(page)
        self.order_summary_data = Text(page, self.locators.order_summary_data, 'Order Summary Data')
        self.delivery_info = Text(page, self.locators.delivery_data, 'Delivery Info')
        self.delivery_date = Text(page, self.CONFIRMATION, 'Delivery Date')
        self.print_order_confirm_btn = Button(page, self.locators.print_order_confirmation_btn, 'Print Order Confirmation Button')
        self.twitter_link = Link(page, self.locators.twitter, 'Post on Twitter Link')
        self.track_order_link = Link(page, self.locators.track_order_link, 'Track Order Link')

    def check_thanks_text_match(self):
        self.thanks_text.check_have_text(self.EXPECTED_THANKS_TEXT)

    def check_order_completion_data_match_expected(self, expected_address_data: AddAddressRespSchema,
        expected_selected_product_data: SelectedProductData, expected_delivery_data: DeliveryOptionsRespSchema):

        self.delivery_info.check_contain_text(expected_address_data.data.full_name)
        self.delivery_info.check_contain_text(expected_address_data.data.street_address)
        self.delivery_info.check_contain_text(expected_address_data.data.city)
        self.delivery_info.check_contain_text(str(expected_address_data.data.zip_code))
        self.delivery_info.check_contain_text(expected_address_data.data.country)
        self.delivery_info.check_contain_text(str(expected_address_data.data.mobile_num))

        if expected_address_data.data.state:
            self.delivery_info.check_contain_text(expected_address_data.data.state)

        self.delivery_date.check_have_text(f'Your order will be delivered in {expected_delivery_data.data.eta} days.')

        self.basket.product_info.check_have_text(expected_selected_product_data.product_name, nth=0)
        self.basket.product_info.check_contain_text(str(expected_selected_product_data.product_price), nth=1)

        self.order_summary_data.check_contain_text(str(expected_delivery_data.data.price), nth=1)
        self.order_summary_data.check_contain_text(str(expected_selected_product_data.product_price), nth=0)

        product_price = Decimal(str(expected_selected_product_data.product_price))
        self.order_summary_data.check_contain_text(
            str(product_price + expected_delivery_data.data.price), nth=3)

    def print_order_confirmation(self):
        with self.page.context.expect_page() as new_page_info:
            self.print_order_confirm_btn.check_enabled()
            self.print_order_confirm_btn.click()
        new_page_url = new_page_info.value.url
        self.page.bring_to_front()
        new_page = new_page_info.value
        new_page.close()
        return new_page_url

    def get_twitter_repost_link(self):
        return self.twitter_link.get_attribute('href')

    def click_track_order(self):
        self.track_order_link.click()
