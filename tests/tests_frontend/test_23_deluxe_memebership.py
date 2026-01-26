import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from data.generators.order_generator import pick_product_to_purchase
from pages.login_page import LoginPage
from tests.tests_frontend.frontend_helpers import log_in_user, log_out_and_log_in, find_out_product_price
from utils.assertions.basket_assertions import assert_price_changes_for_deluxe_member
from utils.assertions.e_wallet_assertions import assert_balance_changes_after_paying_membership_fee

@pytest.mark.smoke
@pytest.mark.usefixtures('close_cookies_banner')
@allure.feature('Deluxe Membership')
@allure.story('Valid deluxe membership flow')
@allure.title('Membership text appears on page and fee is paid')
class TestDeluxeMembership:
    def test_membership_text_appears_on_page_and_fee_is_paid(self, deluxe_membership_page, sum_deposited_into_e_wallet,
        digital_wallet, payment_options_page, get_headers):

        deposit, balance_before_deposit = sum_deposited_into_e_wallet

        deluxe_membership_page.open(PlaywrightEndpoints.DELUXE_MEMBERSHIP)
        fee = deluxe_membership_page.see_membership_fee()

        deluxe_membership_page.become_member()
        payment_options_page.pay_with_digital_wallet()

        deluxe_membership_page.check_membership_text_appears_on_page()

        balance = digital_wallet.get_digital_wallet_balance(
            headers=get_headers
        )

        assert_balance_changes_after_paying_membership_fee(
            expected_balance=balance,
            current_balance=deposit + balance_before_deposit,
            fee=fee
        )

    @pytest.mark.delete_product
    def test_deluxe_membership_offers_sales(self, put_product_into_basket, basket_page, user_register_data_via_ui,
        deluxe_membership_page):

        log_out_and_log_in(
            current_page=deluxe_membership_page,
            login_data=user_register_data_via_ui
        )

        selected_product = pick_product_to_purchase(available='sale')
        old_price = find_out_product_price(selected_product)
        put_product_into_basket(selected_product)

        basket_page.open(PlaywrightEndpoints.BASKET)
        new_price = basket_page.get_total_price()

        assert_price_changes_for_deluxe_member(
            normal_price=old_price,
            price_for_deluxe_member=new_price
        )

    @pytest.mark.delete_card
    @pytest.mark.delete_address
    @pytest.mark.delete_product
    def test_deluxe_membership_offers_free_fast_delivery(self, get_headers, create_address, put_product_into_basket,
        checkout_page, user_register_data_via_ui, deluxe_membership_page, payment_options_page,
        navigate_to_payment_options_page):

        create_address(headers=get_headers)

        selected_product = pick_product_to_purchase(available='sale')
        put_product_into_basket(selected_product)

        navigate_to_payment_options_page(delivery_option=3)
        payment_options_page.select_card_and_proceed_to_checkout()

        checkout_page.check_deluxe_membership_offers_free_fast_delivery()
