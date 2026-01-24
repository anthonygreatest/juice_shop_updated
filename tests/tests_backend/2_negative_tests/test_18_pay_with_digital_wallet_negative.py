from http import HTTPStatus

import allure
import pytest

from data.constants import COUPON_DATA
from utils.assertions.base_assertions import assert_status_code
from utils.helper import prepare_raw_checkout_payload, prepare_missing_headers


@allure.feature('Digital Wallet')
@allure.story('Invalid digital wallet flow')
class TestPayWithDigitalWalletNegative:

    @allure.title('User not able to pay with digital wallet with insufficient balance')
    def test_pay_with_digital_wallet_insufficient_balance(self, login_response, create_address, headers_with_auth,
        create_credit_card, raw_api_client, add_product_to_basket, digital_wallet):

        address_set = create_address.added_address

        card_set = create_credit_card.added_card

        checkout_data = prepare_raw_checkout_payload(
            address_id=address_set.data.id,
            card_id=card_set.data.id,
            digital_wallet=True
        )

        response = raw_api_client.finalize_order_at_checkout(
            endpoint='checkout',
            basket_id=login_response.authentication.bid,
            data=checkout_data,
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.INTERNAL_SERVER_ERROR)

    @pytest.mark.skip
    @allure.title('User not able to pay with digital wallet with missing headers')
    def test_pay_with_digital_wallet_missing_auth(self, headers_with_auth, create_address, login_response,
        create_credit_card, checkout_factory, raw_api_client):

        address_set = create_address.added_address

        card_set = create_credit_card.added_card

        checkout_data = prepare_raw_checkout_payload(
            address_id = address_set.data.id,
            card_id = card_set.data.id,
            digital_wallet = True,
            coupon = COUPON_DATA
        )

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header='Authorization'
        )

        response = raw_api_client.finalize_order_at_checkout(
            endpoint='checkout',
            basket_id = login_response.authentication.bid,
            data = checkout_data,
            headers = bad_headers
        )

        assert_status_code(response, HTTPStatus.UNAUTHORIZED)