import re
from decimal import Decimal

from components.basket_component import BasketComponent
from components.navbar_component import NavbarMenuComponent
from components.toast_component import ToastComponent
from data.locators.basket_page_locators import BasketLocators
from elements.button import Button
from elements.text import Text
from pages.base_page import BasePage
from pages.mixins import NegativeTestsMixin


class BasketPage(BasePage, NegativeTestsMixin):

    PRODUCT_OUT_OF_STOCK = 'We are out of stock! Sorry for the inconvenience.'
    ONLY_ONE_PRODUCT_AVAILABLE = 'You can order only up to 1 items of this product.'

    def __init__(self, page):
        super().__init__(page)
        self.locators = BasketLocators()
        self.basket = BasketComponent(page)
        self.navbar = NavbarMenuComponent(page)
        self.total_price = Text(page, self.locators.total_price, 'Total Price')
        self.checkout_btn = Button(page, self.locators.checkout_btn, 'Checkout Button')
        self.toast = ToastComponent(page)

    def check_product_in_basket_matches_added(self, added_product):
        self.basket.product_info.check_have_text(added_product, nth=1)

    def check_num_of_products_in_basket_matches_notifications_cnt(self, num_of_products_in_basket):
        self.navbar.notifications.check_have_text(str(num_of_products_in_basket))

    def delete_product_from_basket(self):
        self.basket.change_quantity_btn.check_enabled(nth=-1)
        self.basket.click_remove_product_button()

    def plus_one(self):
        self.basket.change_quantity_btn.check_enabled(nth=1)
        self.basket.click_add_one_more_button()

    def minus_one(self):
        self.basket.change_quantity_btn.check_enabled(0)
        self.basket.click_remove_one_button()

    def check_total_price(self, expected_price):
        self.total_price.check_visible()
        self.total_price.check_contain_text(str(expected_price))

    def click_checkout(self):
        self.checkout_btn.check_enabled()
        self.checkout_btn.click()

    def check_checkout_button_remains_disabled(self):
        self.checkout_btn.check_disabled()

    def check_out_of_stock_toast_appears_on_page(self):
        self.toast.check_toast_text(re.compile(f'{self.PRODUCT_OUT_OF_STOCK}|{self.ONLY_ONE_PRODUCT_AVAILABLE}'))

    def get_total_price(self):
        return Decimal(self.total_price.get_text()[12:-1])