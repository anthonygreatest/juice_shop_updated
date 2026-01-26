from decimal import Decimal

from components.card_form_component import CardFormComponent
from components.coupon_form_component import CouponFormComponent
from components.toast_component import ToastComponent
from data.locators.payment_options_page_locators import PaymentOptionsPageLocators
from elements.button import Button
from elements.input import Input
from elements.link import Link
from elements.text import Text
from pages.base_page import BasePage
from pages.mixins import LinkAccessMixin, NegativeTestsMixin
from utils.schemas.add_credit_card_request import AddCreditCardRequest


class PaymentOptionsPage(BasePage, LinkAccessMixin, NegativeTestsMixin):


    STRIPE_LINK = 'https://pwning.owasp-juice.shop/companion-guide/latest/part3/donations.html'
    SPREADSHIRT_US_LINK = 'http://shop.spreadshirt.com/juiceshop'
    SPREADSHIRT_DE_LINK = 'http://shop.spreadshirt.de/juiceshop'
    STICKER_YOU_LINK = 'https://www.stickeryou.com/products/owasp-juice-shop/794'
    LEANPUB_LINK = 'http://leanpub.com/juice-shop'
    OPENSEA_LINK = 'https://opensea.io/collection/juice-shop'
    EMPTY_NAME = 'Please provide a name.'
    EMPTY_CARD_NUM = 'Please enter your card number.'
    EMPTY_EXP_MONTH = 'Please enter an expiry month.'
    EMPTY_EXP_YEAR = 'Please enter an expiry year.'
    INVALID_CARD_NUM = 'Please enter a valid sixteen digit card number.'
    WRONG_LENGTH_COUPON = 'Coupon code must be 10 characters long.'
    INVALID_COUPON = 'Invalid coupon.'
    CARD_ADDED_TEXT = lambda self, card: f'Your card ending with {card[12:]} has been saved for your convenience.'

    def __init__(self, page):
        super().__init__(page)
        self.locators = PaymentOptionsPageLocators()
        self.card_form = CardFormComponent(page)
        self.card_info = Text(page, self.locators.card_data, 'Card Info')
        self.toast = ToastComponent(page)
        self.continue_btn = Button(page, self.locators.continue_btn, 'Continue to checkout')
        self.open_other_payment_options_form = Button(page, self.locators.open_other_payment_options_form, 'Open other payment options')
        self.e_wallet_btn = Button(page, self.locators.pay_btn, 'Pay with e-wallet')
        self.wallet_balance = Text(page, self.locators.wallet_balance_text, 'Wallet Balance')
        self.coupon_form = CouponFormComponent(page)
        self.coupon_applied_text = Text(page, self.locators.success_text, 'Coupon applied')
        self.field_error = Text(page, self.ERROR, 'Field error')
        self.open_coupon_form_btn = Button(page, self.locators.open_coupon_form, 'Open coupon form')
        self.redeem_btn = Button(page, self.locators.redeem_btn, 'Redeem')
        self.form_error = Text(page, self.FORM_ERROR, 'Form error')

    def proceed_to_checkout(self):
        self.continue_btn.check_enabled()
        self.continue_btn.click()

    def check_card_data_on_page_matches_expected(self, expected_card_data: dict):
        self.card_info.check_have_text(expected_card_data['full_name'], nth=2)
        self.card_info.check_have_text('*' * 12 + str(expected_card_data['card_num'])[12:], nth=1)
        self.card_info.check_have_text(f"{expected_card_data['exp_month']}/{expected_card_data['exp_year']}", nth=3)

    def check_card_added_toast_appears_on_page(self, card):
        self.toast.check_toast_text(self.CARD_ADDED_TEXT(str(card['card_num'])))

    def open_other_payment_options(self):
        self.open_other_payment_options_form.check_enabled()
        self.open_other_payment_options_form.click()

    def get_outer_source_link(self, link):
        link = Link(self.page, link, 'Outer resource Link')
        return link.get_attribute('href')

    def get_price_on_pay_button(self):
        return Decimal(self.e_wallet_btn.get_text(nth=1)[5:9])

    def pay_with_digital_wallet(self):
        self.e_wallet_btn.check_enabled(nth=1)
        self.e_wallet_btn.click(nth=1)

    def open_coupon_form(self):
        self.open_coupon_form_btn.check_enabled()
        self.open_coupon_form_btn.click()

    def activate_coupon(self):
        self.open_coupon_form()
        sale, coupon = self.coupon_form.get_coupon()
        self.coupon_form.fill_and_redeem(coupon)
        return sale

    def select_card_and_proceed_to_checkout(self):
        self.card_form.select_card()
        self.proceed_to_checkout()

    def check_coupon_applied_text_matches_expected(self, expected_sale):
        self.coupon_applied_text.check_have_text(self.coupon_form.COUPON_APPLIED_TEXT(expected_sale))

    def check_proceed_to_checkout_button_remains_disabled(self):
        self.continue_btn.check_disabled()

    def check_submit_button_remains_disabled(self):
        self.card_form.submit_btn.check_disabled()

    def check_empty_field_error_appears_on_page(self, expected_error):
        self.field_error.check_have_text(expected_error)

    def check_invalid_field_error_appears_on_page(self, expected_error):
        self.field_error.check_have_text(expected_error)

    def check_e_wallet_button_remains_disabled(self):
        self.e_wallet_btn.check_disabled()

    def check_redeem_button_remains_disabled(self):
        self.redeem_btn.check_disabled()

    def check_wrong_coupon_error_appears_on_page(self):
        self.form_error.check_have_text(self.INVALID_COUPON)
