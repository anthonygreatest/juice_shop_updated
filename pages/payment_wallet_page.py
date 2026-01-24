from components.card_form_component import CardFormComponent
from data.locators.digital_wallet_page_locators import DigitalWalletPageLocators
from elements.button import Button
from pages.base_page import BasePage
from pages.mixins import NegativeTestsMixin


class PaymentWalletPage(BasePage, NegativeTestsMixin):

    def __init__(self, page):
        super().__init__(page)
        self.locators = DigitalWalletPageLocators()
        self.continue_btn = Button(page, self.locators.continue_btn, 'Continue Button')
        self.card_form = CardFormComponent(page)

    def click_continue(self):
        self.continue_btn.check_enabled()
        self.continue_btn.click()

    def select_card(self):
        self.card_form.select_card()
        self.click_continue()

    def check_continue_button_remains_disabled(self):
        self.continue_btn.check_disabled()
