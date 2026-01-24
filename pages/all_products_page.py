import re
from components.navbar_component import NavbarMenuComponent
from components.product_card_component import ProductCardComponent
from components.toast_component import ToastComponent
from data.locators.all_products_locators import AllProductsLocators
from elements.button import Button
from elements.dropdown import Dropdown
from elements.text import Text
from pages.base_page import BasePage
from pages.mixins import LocalizationMixin


class AllProductsPage(BasePage, LocalizationMixin):

    PRODUCT_OUT_OF_STOCK = 'We are out of stock! Sorry for the inconvenience.'
    ONLY_ONE_PRODUCT_AVAILABLE = 'You can order only up to 1 items of this product.'

    LANGUAGE_CHANGED_TOAST = lambda self, language: f'Language has been changed to {language}'

    def __init__(self, page):
        super().__init__(page)
        self.locators = AllProductsLocators()
        self.navbar = NavbarMenuComponent(page)
        self.product_card = ProductCardComponent(page)
        self.toast = ToastComponent(page)
        self.add_button = Button(page, self.locators.add_to_basket_btn, 'Add product Button')
        self.pagination_btn = Button(page, self.locators.pagination_dropdown, 'Pagination')
        self.next_page_btn = Button(page, self.locators.next_page_btn, 'Next page')
        self.previous_page_btn = Button(page, self.locators.previous_page_btn, 'Previous page')
        self.page_number = Text(page, self.locators.page_number, 'Page number')
        self.all_products_heading = Text(page, self.locators.all_products_heading, 'All products heading')

    def check_account_name_matches_email(self, text):
        self.navbar.click_account_menu()
        self.navbar.account_name.check_have_text(text)

    def find_product(self, product):
        self.navbar.click_open_search()
        self.navbar.fill_in_search_field(product)
        self.navbar.click_close_search()

    def add_to_basket(self):
        self.add_button.check_enabled()
        self.add_button.click()

    def find_and_add_product_to_basket(self, product):
        self.find_product(product)
        self.add_to_basket()

    def check_product_added_toast_appears_on_page(self, selected_product):
        self.toast.check_toast_text(self.locators.success_added_text(selected_product))

    def go_to_account_section(self, section_locator, subsection_locator):
        self.navbar.click_account_menu()
        section = Button(self.page, section_locator, 'Section')
        section.hover()
        subsection = Button(self.page, subsection_locator, 'Subsection')
        subsection.check_enabled()
        subsection.click()

    def go_to_menu_section(self, section_locator):
        self.navbar.click_side_menu()
        section = Button(self.page, section_locator, 'Section')
        section.check_enabled()
        section.click()

    def count_products_on_page(self):
        return self.page.locator(self.locators.items_on_page).count()

    def show_more_items_on_page(self, number):
        self.pagination_btn.scroll_into_view_if_needed()
        self.pagination_btn.check_enabled()
        self.pagination_btn.click()
        items_list = Dropdown(self.page, self.locators.number_on_page(number), 'Items per page')
        items_list.click()

    def go_to_next_page(self):
        self.next_page_btn.scroll_into_view_if_needed()
        self.next_page_btn.check_enabled()
        self.next_page_btn.click()

    def go_to_previous_page(self):
        self.previous_page_btn.scroll_into_view_if_needed()
        self.previous_page_btn.check_enabled()
        self.previous_page_btn.click()

    def check_page_number_matches_expected(self, expected_page_number):
        self.page_number.check_contain_text(expected_page_number)

    def check_language_switched_toast_appears_on_page(self, language):
        self.toast.check_toast_text(self.LANGUAGE_CHANGED_TOAST(language))

    def check_heading_language_gets_switched_to_another_language(self, text):
        self.all_products_heading.check_have_text(text)

    def check_account_menu_shows_only_login_for_unlogged_user(self, expected_text):
        self.navbar.menu_sections.check_contain_text(expected_text)

    def check_out_of_stock_toast_appears_on_page(self):
        self.toast.check_toast_text(re.compile(f'{self.PRODUCT_OUT_OF_STOCK}|{self.ONLY_ONE_PRODUCT_AVAILABLE}'))
