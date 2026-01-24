import json
from dataclasses import asdict

import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from pages.payment_options_page import PaymentOptionsPage
from tests.tests_frontend.frontend_helpers import prepare_card_payload_for_ui



@pytest.mark.screenshot
@allure.feature('Credit Card')
@allure.story('Invalid credit card flow')
@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.delete_card
class TestCreditCardNegative:

    @allure.title('User not able to add credit card with empty fields')
    @pytest.mark.parametrize('missing_field, expected_error', [
        ('full_name', PaymentOptionsPage.EMPTY_NAME),
        ('card_num', PaymentOptionsPage.EMPTY_CARD_NUM),
        ('exp_month', PaymentOptionsPage.EMPTY_EXP_MONTH),
        ('exp_year', PaymentOptionsPage.EMPTY_EXP_YEAR),
    ])
    def test_add_credit_card_empty_fields(self, payment_options_page, missing_field, expected_error):

        card_data = prepare_card_payload_for_ui()
        card_data.pop(missing_field)

        payment_options_page.open(PlaywrightEndpoints.PAYMENT_OPTIONS)
        payment_options_page.reload()

        payment_options_page.card_form.fill(
            **card_data
        )

        payment_options_page.card_form.leave_fields_empty(missing_field)

        payment_options_page.check_submit_button_remains_disabled()
        payment_options_page.check_empty_field_error_appears_on_page(
            expected_error=expected_error
        )


    @allure.title('User not able to add credit card with invalid card number')
    @pytest.mark.parametrize('field, card_num', [
        ('card_num', '1' * 15),
        ('card_num', '1' * 17)
    ])
    def test_add_credit_card_with_invalid_card_number(self, payment_options_page, field, card_num):

        card_data = prepare_card_payload_for_ui()

        card_data[field] = card_num

        payment_options_page.open(PlaywrightEndpoints.PAYMENT_OPTIONS)
        payment_options_page.reload()

        payment_options_page.card_form.fill(
            **card_data
        )
        payment_options_page.card_form.card_num_input.blur()

        payment_options_page.check_submit_button_remains_disabled()
        payment_options_page.check_invalid_field_error_appears_on_page(PaymentOptionsPage.INVALID_CARD_NUM)

    @pytest.mark.delete_product
    @pytest.mark.delete_address
    @allure.title('User not able to proceed to checkout without card')
    def test_user_not_able_to_proceed_to_checkout_without_card_selected(self, user_at_checkout, payment_options_page):

        payment_options_page.check_proceed_to_checkout_button_remains_disabled()



