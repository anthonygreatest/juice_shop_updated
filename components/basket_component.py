import re
from decimal import Decimal

from playwright.sync_api import Page

from components.base_component import BaseComponent
from data.locators.basket_page_locators import BasketLocators
from elements.button import Button
from elements.text import Text


class BasketComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = BasketLocators
        # self.products_in_basket = Text(page, self.locators.products_in_basket, 'Products in basket')
        self.product_info = Text(page, self.locators.product_info, 'Product info')
        self.random_product_in_basket = Text(page, self.locators.random_product_in_basket, 'Product in basket')
        self.change_quantity_btn = Button(page, self.locators.item_quantity_btn, 'Change quantity button')

    def count_products_in_basket(self):
        return self.random_product_in_basket.count_elements()

    def click_remove_product_button(self):
        self.change_quantity_btn.click(nth=-1, specified_name=' (delete from basket)')

    def click_add_one_more_button(self):
        self.change_quantity_btn.click(nth=1, specified_name=' (+1)')

    def click_remove_one_button(self):
        self.change_quantity_btn.click(nth=0, specified_name=' (-1)')

    def get_product_quantity(self):
        item = self.random_product_in_basket.get_locator()
        locator = item.locator('span', has_text=re.compile(r'\d+'))
        text = locator.text_content().strip()
        return int(text)

    def get_product_price(self):
        return Decimal(self.product_info.get_text(nth=3)[:-1])
