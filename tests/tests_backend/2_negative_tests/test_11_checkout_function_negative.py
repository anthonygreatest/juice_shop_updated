import json
from http import HTTPStatus

import allure
import pytest
from data.constants import COUPON_DATA
from data.endpoints import Endpoints
from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import prepare_raw_checkout_payload, prepare_checkout_with_missing_fields, prepare_missing_headers


@allure.feature('Checkout')
@allure.story('Invalid checkout flow')
@pytest.mark.delete_address
@pytest.mark.delete_card
class TestCheckoutNegative:

    @allure.title('User not able to go to checkout with invalid data')
    @pytest.mark.parametrize('field, value, expected', [
        ('addressId', 0, HTTPStatus.BAD_REQUEST),
        ('addressId', 'abc', HTTPStatus.BAD_REQUEST),
        ('addressId', True, HTTPStatus.BAD_REQUEST),
        ('addressId', None, HTTPStatus.BAD_REQUEST),
        ('deliveryMethodId', 0, HTTPStatus.BAD_REQUEST),
        ('deliveryMethodId', 'abc', HTTPStatus.BAD_REQUEST),
        ('deliveryMethodId', True, HTTPStatus.BAD_REQUEST),
        ('deliveryMethodId', None, HTTPStatus.BAD_REQUEST),
        ('deliveryMethodId', 4, HTTPStatus.BAD_REQUEST),
        ('deliveryMethodId', 3, HTTPStatus.OK),
        ('paymentId', 0, HTTPStatus.BAD_REQUEST),
        ('paymentId', 'abc', HTTPStatus.BAD_REQUEST),
        ('paymentId', True, HTTPStatus.BAD_REQUEST),
        ('paymentId', None, HTTPStatus.BAD_REQUEST)
    ])
    def test_checkout_with_invalid_data(self, raw_api_client, create_address, headers_with_auth, login_response,
        create_credit_card, field, value, expected):

        address_set = create_address.added_address

        card_set = create_credit_card.added_card

        data = prepare_raw_checkout_payload(
            address_id=address_set.data.id,
            card_id=card_set.data.id,
            digital_wallet=False
        )

        data['orderDetails'][field] = value

        response = raw_api_client.finalize_order_at_checkout(
            endpoint='checkout',
            basket_id=login_response.authentication.bid,
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to go to checkout with missing fields')
    @pytest.mark.parametrize('missing_field, schema, expected', [
        ('addressId', 'inner', HTTPStatus.BAD_REQUEST),
        ('deliveryMethodId', 'inner', HTTPStatus.BAD_REQUEST),
        ('paymentId', 'inner', HTTPStatus.BAD_REQUEST),
        ('couponData', 'outer', HTTPStatus.OK),
        ('orderDetails', 'outer', HTTPStatus.BAD_REQUEST),
    ])
    def test_checkout_missing_fields(self, raw_api_client, create_address, login_response, headers_with_auth,
    create_credit_card, missing_field, schema, expected):

        address_set = create_address.added_address

        card_set = create_credit_card.added_card

        data = prepare_raw_checkout_payload(
            address_id=address_set.data.id,
            card_id=card_set.data.id,
            digital_wallet=False
        )

        invalid_data = prepare_checkout_with_missing_fields(
           schema=schema,
           data=data,
            missing_field=missing_field
        )

        response = raw_api_client.finalize_order_at_checkout(
            endpoint='checkout',
            basket_id=login_response.authentication.bid,
            data=invalid_data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to go to checkout with wrong HTTP method')
    def test_checkout_wrong_method(self, raw_api_client, create_credit_card, headers_with_auth, create_address,
        login_response):

        address_set = create_address.added_address

        card_set = create_credit_card.added_card

        params = prepare_raw_checkout_payload(
            address_id=address_set.data.id,
            card_id=card_set.data.id,
            digital_wallet=False
        )

        response = raw_api_client.get_with_id(
            endpoint='checkout',
            endpoint_id=login_response.authentication.bid,
            params=params,
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.INTERNAL_SERVER_ERROR)

    @allure.title('User not able to go to checkout with missing headers')
    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [400, 415, 500]),
        ('Authorization', [401])
    ])
    def test_checkout_missing_headers(self, checkout, raw_api_client, login_response, headers_with_auth, create_address,
        create_credit_card, missing_header, codes):

        address_set = create_address.added_address

        card_set = create_credit_card.added_card

        data = prepare_raw_checkout_payload(
            address_id=address_set.data.id,
            card_id=card_set.data.id,
            digital_wallet=False
        )

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header=missing_header
        )

        response = raw_api_client.post_with_id_with_raw_headers(
            endpoint='checkout',
            endpoint_id=login_response.authentication.bid,
            data=data,
            headers=bad_headers
        )

        assert_status_code_among_expected(response, codes)
