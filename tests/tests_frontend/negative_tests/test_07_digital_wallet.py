import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from data.generators.order_generator import pick_product_to_purchase
from pages.digital_wallet_page import DigitalWalletPage
from utils.helper import deposit_to_digital_wallet_payload, select_delivery_speed


@pytest.mark.screenshot
@allure.feature('Digital Wallet')
@allure.story('Invalid digital wallet flow')
@pytest.mark.usefixtures('close_cookies_banner')
class TestDigitalWalletNegative:

    @allure.title('User not able to purchase with insufficient balance on digital wallet')
    @pytest.mark.delete_address
    @pytest.mark.delete_product
    @pytest.mark.delete_card
    def test_purchase_with_insufficient_balance_on_digital_wallet(self, get_headers, create_address,
        create_credit_card, put_product_into_basket, navigate_to_payment_options_page, payment_options_page):

        create_address(headers=get_headers)
        create_credit_card(headers=get_headers)
        delivery_option = select_delivery_speed().delivery_date

        selected_product = pick_product_to_purchase(available='expensive_product')
        put_product_into_basket(selected_product)

        navigate_to_payment_options_page(delivery_option)

        payment_options_page.check_e_wallet_button_remains_disabled()

    @allure.title('User not able to deposit invalid sum into digital wallet')
    @pytest.mark.delete_card
    @pytest.mark.parametrize('random_sum, expected_error', [
        ('9', DigitalWalletPage.INVALID_SUM),
        ('1001', DigitalWalletPage.INVALID_SUM),
        ('', DigitalWalletPage.EMPTY_SUM)
    ])
    def test_deposit_invalid_sum_into_digital_wallet(self, digital_wallet_page, random_sum, expected_error):

        digital_wallet_page.open(PlaywrightEndpoints.DIGITAL_WALLET)

        digital_wallet_page.enter_sum(
            random_sum
        )

        digital_wallet_page.check_invalid_data_error_appears_on_page(expected_error=expected_error)
        digital_wallet_page.check_deposit_button_remains_disabled()

    @allure.title('User not able to deposit without card')
    @pytest.mark.delete_card
    def test_not_able_to_deposit_without_card(self, digital_wallet_page, payment_wallet_page, create_credit_card,
        get_headers):

        card_data = create_credit_card(headers=get_headers)

        deposit_sum = deposit_to_digital_wallet_payload(
            payment_id=card_data.added_card.data.id,
            balance='random'
        ).balance

        digital_wallet_page.open(PlaywrightEndpoints.DIGITAL_WALLET)
        digital_wallet_page.deposit_money_into_wallet(deposit_sum)

        payment_wallet_page.check_continue_button_remains_disabled()


