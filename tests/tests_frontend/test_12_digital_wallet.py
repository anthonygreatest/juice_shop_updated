import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from tests.tests_frontend.frontend_helpers import calculate_current_balance
from utils.helper import deposit_to_digital_wallet_payload


@allure.feature('Digital Wallet')
@allure.story('Valid digital wallet flow')
@pytest.mark.delete_card
@pytest.mark.usefixtures('close_cookies_banner')
class TestDigitalWallet:

    @allure.title('Deposited sum appears on page')
    def test_deposited_sum_appears_on_page(self, digital_wallet_page, payment_wallet_page,
        get_headers, create_credit_card):

        card_data = create_credit_card(headers=get_headers)

        deposit_sum = deposit_to_digital_wallet_payload(
            payment_id=card_data.added_card.data.id,
            balance='random'
        ).balance

        digital_wallet_page.open(PlaywrightEndpoints.DIGITAL_WALLET)
        money_before = digital_wallet_page.get_current_balance()

        digital_wallet_page.deposit_money_into_wallet(deposit_sum)
        payment_wallet_page.select_card()

        digital_wallet_page.check_current_balance_money_matches_expected(
            expected_sum=deposit_sum + money_before
        )

    @allure.title('Deposited sum success toast appears on page')
    def test_success_deposit_toast_appears_on_page(self, digital_wallet_page, payment_wallet_page,
        get_headers, create_credit_card):

        card_data = create_credit_card(headers=get_headers)

        deposit_sum = deposit_to_digital_wallet_payload(
            payment_id=card_data.added_card.data.id,
            balance='random'
        ).balance

        digital_wallet_page.open(PlaywrightEndpoints.DIGITAL_WALLET)
        digital_wallet_page.get_current_balance()

        digital_wallet_page.deposit_money_into_wallet(deposit_sum)
        payment_wallet_page.select_card()

        digital_wallet_page.check_money_deposited_toast_appears_on_page()

    @pytest.mark.delete_address
    @pytest.mark.delete_product
    @pytest.mark.delete_card
    @allure.title('User able to pay with digital wallet')
    def test_pay_with_digital_wallet(self, user_at_checkout,
        payment_options_page, digital_wallet_page, checkout_page):

        current_balance = calculate_current_balance(deposit_data=user_at_checkout.deposit_data)
        total_price = payment_options_page.get_price_on_pay_button()

        payment_options_page.pay_with_digital_wallet()
        checkout_page.place_your_order_and_pay()

        digital_wallet_page.open(PlaywrightEndpoints.DIGITAL_WALLET)

        digital_wallet_page.check_current_balance_money_matches_expected(
            expected_sum=current_balance - total_price
        )

    @allure.title('Crypto wallet requires installation')
    def test_crypto_wallet_requires_installation(self, digital_wallet_page, crypto_wallet_page):

        digital_wallet_page.open(PlaywrightEndpoints.DIGITAL_WALLET)
        digital_wallet_page.click_crypto_wallet_link()

        crypto_wallet_page.click_connect_metamask()

        crypto_wallet_page.check_metamask_requires_installation_toast_appears()








