from decimal import Decimal
from components.toast_component import ToastComponent
from data.locators.digital_wallet_page_locators import DigitalWalletPageLocators
from elements.button import Button
from elements.input import Input
from elements.link import Link
from elements.text import Text
from pages.base_page import BasePage
from pages.mixins import NegativeTestsMixin


class DigitalWalletPage(BasePage, NegativeTestsMixin):

    MONEY_DEPOSITED_TEXT = 'Wallet successfully charged.'
    INVALID_SUM = 'You can add a minimum of 10¤ and only up to 1000¤.'
    EMPTY_SUM = 'Please enter an amount'

    def __init__(self, page):
        super().__init__(page)
        self.locators = DigitalWalletPageLocators()
        self.deposit_amount = Input(page, self.locators.amount_field, 'Deposit amount Input')
        self.deposit_amount_btn = Button(page, self.locators.deposit_btn, 'Deposit Button')
        self.current_balance = Text(page, self.locators.sum_text, 'Balance')
        self.deposit_toast = ToastComponent(page)
        self.crypto_link = Link(page, self.locators.crypto_wallet_link, 'Crypto Wallet Link')
        self.field_error = Text(page, self.ERROR, 'Field error')

    def enter_sum(self, deposit_sum):
        self.deposit_amount.fill(deposit_sum)
        self.deposit_amount.check_have_value(deposit_sum)
        self.deposit_amount.blur()

    def click_deposit(self):
        self.deposit_amount_btn.check_enabled()
        self.deposit_amount_btn.click()

    def get_current_balance(self):
        balance = self.current_balance.get_text()
        return Decimal(str(balance))

    def check_money_deposited_toast_appears_on_page(self):
        self.deposit_toast.check_toast_text(self.MONEY_DEPOSITED_TEXT)

    def deposit_money_into_wallet(self, deposit_sum):
        self.enter_sum(
            str(deposit_sum)
        )
        self.click_deposit()

    def check_current_balance_money_matches_expected(self, expected_sum):
        self.current_balance.check_have_text(str(expected_sum))
        print(self.current_balance.get_text())

    def click_crypto_wallet_link(self):
        self.crypto_link.click()

    def check_invalid_data_error_appears_on_page(self, expected_error):
        self.field_error.check_have_text(expected_error)

    def check_deposit_button_remains_disabled(self):
        self.deposit_amount_btn.check_disabled()
