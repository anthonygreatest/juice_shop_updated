from http import HTTPStatus

import allure
import pytest

from utils.assertions.base_assertions import assert_status_code
from utils.assertions.e_wallet_assertions import assert_balance_changes_after_purchase
from utils.helper import prepare_checkout_response
from utils.schemas.get_order_history_schema import GetOrderHistoryListSchema
from utils.validators import validate_response


@pytest.mark.delete_address
@pytest.mark.delete_card
@allure.feature('Digital wallet')
@allure.story('Valid pay with digital wallet flow')
class TestPayWithDigitalWallet:

    @allure.title('User able to pay with digital wallet')
    def test_user_able_to_pay_with_e_wallet(self, checkout_factory, headers_with_auth):

        checkout_data = checkout_factory(e_wallet=True, headers=headers_with_auth)
        response = checkout_data.checkout_response

        assert_status_code(response, HTTPStatus.OK)

    @allure.title('Balance changes after paying with digital wallet')
    def test_balance_changes_after_paying_with_e_wallet(self, tracking_order,
        checkout_factory, headers_with_auth, digital_wallet, login_response):

        checkout_data = checkout_factory(e_wallet=True, headers=headers_with_auth, login_response=login_response)
        balance_before = checkout_data.balance_before
        checkout_response = prepare_checkout_response(checkout_data)

        response_from_tracking_order = tracking_order.get_tracking_order(
            tracking_id=checkout_response.order_confirmation,
            headers=headers_with_auth
        )

        validated_response = validate_response(GetOrderHistoryListSchema, response_from_tracking_order.json())

        balance_after = digital_wallet.get_digital_wallet_balance(
            headers=headers_with_auth
        )

        assert_balance_changes_after_purchase(
            balance_before=balance_before,
            expected_balance=balance_after,
            deposit=validated_response
        )