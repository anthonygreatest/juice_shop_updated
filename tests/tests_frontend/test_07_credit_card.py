import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from tests.tests_frontend.frontend_helpers import prepare_card_payload_for_ui


@allure.feature('Credit card')
@allure.story('Valid credit card flow')
@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.delete_card
class TestAddCreditCard:

    @allure.title('Saved card appears on page')
    def test_added_credit_card_saved(self, payment_options_page, add_credit_card):
        card_data = prepare_card_payload_for_ui()

        payment_options_page.open(PlaywrightEndpoints.PAYMENT_OPTIONS)

        payment_options_page.card_form.fill(
            **card_data
        )
        add_credit_card(payment_options_page)

        payment_options_page.check_card_data_on_page_matches_expected(
            expected_card_data=card_data
        )

    @allure.title('Card saved success toast appears on page')
    def test_added_credit_card_toast(self, payment_options_page, add_credit_card):
        card_data = prepare_card_payload_for_ui()

        payment_options_page.open(PlaywrightEndpoints.PAYMENT_OPTIONS)
        payment_options_page.reload()

        payment_options_page.card_form.fill(
            **card_data
        )
        add_credit_card(payment_options_page)

        payment_options_page.check_card_added_toast_appears_on_page(
            card=card_data
        )

