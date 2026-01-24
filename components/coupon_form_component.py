from playwright.sync_api import Page

from components.base_component import BaseComponent
from data.locators.payment_options_page_locators import PaymentOptionsPageLocators
from elements.button import Button
from elements.input import Input
from elements.link import Link
from elements.text import Text


class CouponFormComponent(BaseComponent):

    COUPON_APPLIED_TEXT = lambda self, sale: f'Your discount of {sale}% will be applied during checkout.'

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = PaymentOptionsPageLocators
        self.coupon_input = Input(page, self.locators.coupon_field, 'Coupon')
        self.reddit_link = Link(page, self.locators.reddit_link, 'Reddit')
        self.redeem_btn = Button(page, self.locators.redeem_btn, 'Redeem')
        self.first_post = Link(page, self.locators.first_post, 'First Post on Reddit')
        self.coupon = Text(page, self.locators.coupon, 'Coupon')
        self.sale = Text(page, self.locators.sale, 'Sale')

    def fill(self, coupon):
        self.coupon_input.fill(coupon)
        self.coupon_input.check_have_value(coupon)
        self.coupon_input.blur()

    def click_redeem(self):
        self.redeem_btn.check_enabled()
        self.redeem_btn.click()

    def fill_and_redeem(self, coupon):
        self.fill(coupon)
        self.click_redeem()

    def get_coupon(self):
        with self.page.context.expect_event('page') as new_page:
            self.reddit_link.click()
        reddit_page = new_page.value
        reddit_page.wait_for_selector(self.locators.first_post, state='visible')
        reddit_page.click(self.locators.first_post)
        reddit_page.wait_for_selector(self.locators.coupon, state='visible')
        coupon = reddit_page.locator(self.locators.coupon).inner_text()
        sale = reddit_page.locator(self.locators.sale).inner_text()[:-1]
        # sale = int(sale_text) / 100
        self.page.bring_to_front()
        reddit_page.close()
        return sale, coupon

