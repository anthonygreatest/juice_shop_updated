from components.basket_component import BasketComponent
from data.dataclasses.delivery_data import DeliveryData
from data.dataclasses.selected_product_data import SelectedProductData
from data.locators.checkout_page_locators import CheckoutPageLocators
from elements.button import Button
from elements.text import Text
from pages.base_page import BasePage
from utils.schemas.add_address_request_schema import AddAddressSchema
from utils.schemas.add_credit_card_request import AddCreditCardRequest


class CheckoutPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.locators = CheckoutPageLocators()
        self.place_order_btn = Button(page, self.locators.place_order_btn, 'Place your order and pay Button')
        self.basket = BasketComponent(page)
        self.card_info = Text(page, self.locators.card_info, 'Card Info')
        self.order_summary_data = Text(page, self.locators.order_summary_data, 'Order summary data')
        self.delivery_info = Text(page, self.locators.delivery_info, 'Delivery Info')

    def place_your_order_and_pay(self):
        self.place_order_btn.check_enabled()
        self.place_order_btn.click()

    def check_checkout_data_matches_expected(self, card_data: AddCreditCardRequest,
        address_data: AddAddressSchema, selected_product_data: SelectedProductData, delivery_data: DeliveryData):

        self.card_info.check_contain_text(card_data.full_name)
        self.card_info.check_contain_text(f'Card ending in {str(card_data.card_num)[12:]}')
        self.delivery_info.check_contain_text(address_data.full_name)
        self.delivery_info.check_contain_text(address_data.street_address)
        self.delivery_info.check_contain_text(address_data.city)
        self.delivery_info.check_contain_text(str(address_data.zip_code))
        self.delivery_info.check_contain_text(address_data.country)
        self.delivery_info.check_contain_text(str(address_data.mobile_num))

        if address_data.state:
            self.delivery_info.check_contain_text(address_data.state)

        self.basket.product_info.check_have_text(selected_product_data.product_name, nth=1)
        self.basket.product_info.check_contain_text(str(selected_product_data.product_price), nth=3)

        self.order_summary_data.check_contain_text(str(delivery_data.delivery_price), nth=1)
        self.order_summary_data.check_contain_text(str(selected_product_data.product_price), nth=0)
        self.order_summary_data.check_contain_text(
            str(selected_product_data.product_price + delivery_data.delivery_price), nth=3)

    def check_calculated_sale_and_final_price_match_expected(self, expected_sale, expected_final_price):
        self.order_summary_data.check_contain_text(str(expected_sale), nth=2, specified_name=' (sale)')
        self.order_summary_data.check_contain_text(str(expected_final_price), nth=3, specified_name=' (final price)')

    def check_deluxe_membership_offers_free_fast_delivery(self):
        self.order_summary_data.check_contain_text(str(0.00), nth=1)