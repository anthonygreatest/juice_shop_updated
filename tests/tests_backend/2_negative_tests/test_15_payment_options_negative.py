import json
from http import HTTPStatus

import allure
import pytest

from data.endpoints import Endpoints
from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import prepare_missing_headers


@allure.feature('Credit Card')
@allure.story('Invalid credit card flow')
@pytest.mark.delete_card
class TestPaymentOptionsNegative:

    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [200]),
        ('Authorization', [401, 500])
    ])
    @allure.title('User not able to see credit cards with missing headers')
    def test_get_my_payment_options_missing_headers(self, raw_api_client, headers_with_auth, missing_header, codes):

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header=missing_header
        )

        response = raw_api_client.get(
            endpoint='credit_card',
            headers=bad_headers
        )

        assert_status_code_among_expected(response, codes)

    @allure.title('User not able to see credit cards with wrong HTTP method')
    def test_get_my_payment_options_wrong_method(self, raw_api_client, headers_with_auth):

        response = raw_api_client.post(
            endpoint='credit_card',
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.UNAUTHORIZED)

    @allure.title('User not able to delete nonexistent card')
    @pytest.mark.parametrize('card_id, expected', [
        (0, HTTPStatus.BAD_REQUEST),
        ('abc', HTTPStatus.BAD_REQUEST)
    ])
    def test_delete_nonexistent_card(self, credit_card, headers_with_auth, card_id, expected):

        response = credit_card.delete_credit_card(
            card_id=card_id,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)
