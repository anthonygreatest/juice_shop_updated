from playwright.sync_api import Page

from components.base_component import BaseComponent
from data.locators.all_products_locators import AllProductsLocators
from elements.button import Button
from elements.input import Input
from elements.text import Text


class NavbarMenuComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = AllProductsLocators
        self.account_menu = Button(page, self.locators.account_menu, 'Account menu')
        self.account_name = Text(page, self.locators.account_name, 'Account Name')
        self.menu_sections = Button(page, self.locators.menu_sections, 'Menu sections')
        self.open_search_btn = Button(page, self.locators.search_icon, 'Open search')
        self.search_input = Input(page, self.locators.search_input, 'Search')
        self.search = Button(page, self.locators.search_icon, 'Search')
        self.close_search_btn = Button(page, self.locators.close_search_icon, 'Close search')
        self.basket_btn = Button(page, self.locators.go_to_basket_btn, 'Go to basket')
        self.notifications = Text(page, self.locators.notification_basket, 'Notifications in basket')
        self.side_menu = Button(page, self.locators.side_menu, 'Side menu')
        self.choose_lang_btn = Button(page, self.locators.choose_language, 'Choose language')
        self.search_lang_input = Input(page, self.locators.search_language_input, 'Search language')
        self.language_btn = Button(page, self.locators.language, 'Select Language')
        self.language_text = Text(page, self.locators.language_text, 'Selected Language')
        self.logout_btn = Button(page, self.locators.logout, 'Logout')

    def click_account_menu(self):
        self.account_menu.click()

    def click_side_menu(self):
        self.side_menu.check_enabled()
        self.side_menu.click()

    def click_open_search(self):
        self.open_search_btn.click()

    def fill_in_search_field(self, product):
        self.search_input.fill(product)
        self.search_input.check_have_value(product)
        self.search_input.press_enter()

    def click_close_search(self):
        self.close_search_btn.click()

    def click_go_to_basket(self):
        self.basket_btn.check_enabled()
        self.basket_btn.click()
        self.check_current_url('/#/basket')

    def change_language(self, language_prompt):
        self.choose_lang_btn.check_enabled()
        self.choose_lang_btn.click()
        self.search_lang_input.fill(language_prompt)
        self.search_lang_input.check_have_value(language_prompt)
        language_text = self.language_text.get_attribute('aria-label')
        self.language_btn.check_enabled()
        self.language_btn.click()
        return language_text

    def log_out(self):
        self.click_account_menu()
        self.logout_btn.check_enabled()
        self.logout_btn.click()


    # def check_page_number_matches_expected(self, expected_page_num):
    #     self.page_number.check_contain_text(expected_page_num)


    # def get_notifications_num(self):
    #     return self.notifications.get_text()