from http import HTTPStatus

import allure
import pytest
from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import prepare_raw_deposit_payload, prepare_missing_headers


@allure.feature('Digital Wallet')
@allure.story('Invalid digital wallet flow')
class TestDigitalWalletNegative:

    @allure.title('User not able to deposit invalid data to digital wallet')
    @pytest.mark.parametrize('field, value, expected', [
        ('payment_id', 0, HTTPStatus.BAD_REQUEST),
        ('payment_id', True, HTTPStatus.BAD_REQUEST),
        ('payment_id', 'abc', HTTPStatus.BAD_REQUEST),
        ('payment_id', None, HTTPStatus.BAD_REQUEST),
        ('balance', 0, HTTPStatus.BAD_REQUEST),
        ('balance', 1, HTTPStatus.OK),
        ('balance', -10, HTTPStatus.BAD_REQUEST),
        ('balance', 1001, HTTPStatus.BAD_REQUEST),
        ('balance', 'a', HTTPStatus.BAD_REQUEST),
        ('balance', True, HTTPStatus.BAD_REQUEST),
    ])
    def test_digital_wallet_invalid_data(self, create_credit_card, headers_with_auth, raw_api_client, field, value, expected):

        payment_id = create_credit_card.added_card.data.id

        data = prepare_raw_deposit_payload(
            payment_id=payment_id,
            balance='random'
        )

        data[field] = value

        response = raw_api_client.put(
            endpoint='digital_wallet',
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to deposit invalid data to digital wallet')
    @pytest.mark.parametrize('missing_field, expected', [
        ('paymentId', HTTPStatus.PAYMENT_REQUIRED),
        ('balance', HTTPStatus.BAD_REQUEST)
    ])
    def test_digital_wallet_missing_fields(self, create_credit_card, headers_with_auth, raw_api_client, missing_field, expected):
        payment_id = create_credit_card.added_card.data.id

        data = prepare_raw_deposit_payload(
            payment_id=payment_id,
            balance='random'
        )

        data.pop(missing_field)

        response = raw_api_client.put(
            endpoint='digital_wallet',
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to deposit data with wrong HTTP method to digital wallet')
    def test_digital_wallet_wrong_method(self, create_credit_card, headers_with_auth, raw_api_client):
        payment_id = create_credit_card.added_card.data.id

        params = prepare_raw_deposit_payload(
            payment_id=payment_id,
            balance='random'
        )

        response = raw_api_client.get(
            endpoint='digital_wallet',
            params=params,
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.METHOD_NOT_ALLOWED)

    @allure.title('User not able to deposit data with missing headers to digital wallet')
    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [400, 415, 500, 200]),
        ('Authorization', [401])
    ])
    def test_digital_wallet_missing_headers(self, create_credit_card, headers_with_auth, raw_api_client, missing_header, codes):
        payment_id = create_credit_card.added_card.data.id

        data = prepare_raw_deposit_payload(
            payment_id=payment_id,
            balance='random'
        )

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header=missing_header
        )

        response = raw_api_client.get(
            endpoint='digital_wallet',
            params=data,
            headers=bad_headers
        )

        assert_status_code_among_expected(response, codes)

