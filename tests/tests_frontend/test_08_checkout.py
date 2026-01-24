import json

import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from data.locators.payment_options_page_locators import PaymentOptionsPageLocators
from pages.checkout_page import CheckoutPage
from pages.payment_options_page import PaymentOptionsPage
from tests.conftest import login_response
from tests.tests_frontend.frontend_helpers import find_product_by_id
from utils.assertions.tracking_order_assertions import assert_print_order_confirmation_url_matches_expected, \
    assert_twitter_repost_link_matches_expected, assert_outer_source_link_matches_expected
from utils.helper import prepare_checkout_response


@allure.feature('Checkout')
@allure.story('Valid checkout flow')
@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.delete_address
@pytest.mark.delete_card
class TestCheckout:

    @pytest.mark.delete_product
    @allure.title('Added address, credit card, product data appear on checkout page')
    def test_added_data_appears_in_order_summary(self, user_at_checkout, payment_options_page, checkout_page):

        payment_options_page.select_card_and_proceed_to_checkout()

        checkout_page.check_checkout_data_matches_expected(
            card_data=user_at_checkout.card_data,
            address_data=user_at_checkout.address_data,
            selected_product_data=user_at_checkout.selected_product_data,
            delivery_data=user_at_checkout.delivery_data
        )

    @allure.title('Thanks for purchase text appears on page')
    def test_successful_purchase_appears_in_order_completion(self, user_at_checkout, payment_options_page, checkout_page,
        order_completion_page):

        payment_options_page.select_card_and_proceed_to_checkout()

        checkout_page.place_your_order_and_pay()

        order_completion_page.check_thanks_text_match()

    @allure.title('Added address, delivery date, product data appear on order completion page')
    def test_data_match_in_order_completion(self, order_completion_page,
        checkout_factory, get_headers, basket_id):

        checkout_data = checkout_factory(e_wallet=False, headers=get_headers, login_response=basket_id)
        tracking_num = prepare_checkout_response(checkout_data).order_confirmation

        order_completion_page.open(PlaywrightEndpoints().ORDER_COMPLETION(tracking_num=tracking_num))


        order_completion_page.check_order_completion_data_match_expected(
            expected_address_data=checkout_data.address_created,
            expected_selected_product_data=checkout_data.product_name_and_price,
            expected_delivery_data=checkout_data.delivery_selected
        )


    @allure.title('Order info can be printed')
    def test_order_confirmation_is_ready_for_print(self, order_completion_page, checkout_factory, get_headers, basket_id):

        checkout_data = checkout_factory(e_wallet=False, headers=get_headers, login_response=basket_id)
        order_confirmation = prepare_checkout_response(checkout_data).order_confirmation

        order_completion_page.open(PlaywrightEndpoints().ORDER_COMPLETION(order_confirmation))
        new_page_url = order_completion_page.print_order_confirmation()

        expected_url = f'{PlaywrightEndpoints.BASE_URL_FRONT}/ftp/order_{order_confirmation}.pdf'

        assert_print_order_confirmation_url_matches_expected(new_page_url, expected_url)

    @allure.title('Links on page are available')
    @pytest.mark.parametrize('locator, expected_link', [
        (PaymentOptionsPageLocators.stripe, PaymentOptionsPage.STRIPE_LINK),
        (PaymentOptionsPageLocators.spreadshirt_us, PaymentOptionsPage.SPREADSHIRT_US_LINK),
        (PaymentOptionsPageLocators.spreadshirt_de, PaymentOptionsPage.SPREADSHIRT_DE_LINK),
        (PaymentOptionsPageLocators.open_sea, PaymentOptionsPage.OPENSEA_LINK),
        (PaymentOptionsPageLocators.sticker_you, PaymentOptionsPage.STICKER_YOU_LINK),
        (PaymentOptionsPageLocators.lean_pub, PaymentOptionsPage.LEANPUB_LINK),
    ])
    def test_outer_source_links_on_payment_page(self, payment_options_page, locator, expected_link):

        payment_options_page.open(PlaywrightEndpoints.PAYMENT_OPTIONS)
        payment_options_page.open_other_payment_options()

        actual_link = payment_options_page.get_outer_source_link(
            locator
        )

        assert_outer_source_link_matches_expected(actual_link, expected_link)

    @allure.title('User can share order on twitter')
    def test_twitter_link_on_completion_page(self, checkout_factory, order_completion_page, get_headers, basket_id):

        checkout_data = checkout_factory(e_wallet=False, headers=get_headers, login_response=basket_id)
        order_confirmation = prepare_checkout_response(checkout_data).order_confirmation

        order_completion_page.open(PlaywrightEndpoints().ORDER_COMPLETION(order_confirmation))

        purchase_name = checkout_data.product_name_and_price.product_name

        actual_link = order_completion_page.get_twitter_repost_link()

        assert_twitter_repost_link_matches_expected(
            actual_url=actual_link,
            expected_url=order_completion_page.TWITTER_REPOST_LINK(purchase_name)
        )











