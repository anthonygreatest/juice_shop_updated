from http import HTTPStatus

import allure
import pytest

from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import prepare_raw_card_payload, prepare_missing_headers


@allure.feature('Credit Card')
@allure.story('Invalid credit card flow')
@pytest.mark.delete_card
class TestCreditCardNegative:

    @allure.title('User not able to add new card with invalid data')
    @pytest.mark.parametrize('field, value, expected', [
        ('fullName', 0, HTTPStatus.BAD_REQUEST),
        ('fullName', 'a', HTTPStatus.BAD_REQUEST),
        ('fullName', 'Jesse'*100, HTTPStatus.BAD_REQUEST),
        ('fullName', True, HTTPStatus.BAD_REQUEST),
        ('cardNum', True, HTTPStatus.BAD_REQUEST),
        ('cardNum', 0, HTTPStatus.BAD_REQUEST),
        ('cardNum', 'a', HTTPStatus.BAD_REQUEST),
        ('cardNum', int('1'*17), HTTPStatus.BAD_REQUEST),
        ('cardNum', int('1'*16), HTTPStatus.CREATED),
        ('expYear', '2079', HTTPStatus.BAD_REQUEST),
        ('expYear', '2080', HTTPStatus.CREATED),
        ('expYear', '2100', HTTPStatus.BAD_REQUEST),
        ('expYear', '2099', HTTPStatus.CREATED),
        ('expYear', 2080, HTTPStatus.CREATED),
        ('expYear', 'abc', HTTPStatus.BAD_REQUEST),
        ('expMonth', '13', HTTPStatus.BAD_REQUEST),
        ('expMonth', '1', HTTPStatus.CREATED),
        ('expMonth', 'abc', HTTPStatus.BAD_REQUEST),
        ('expMonth', True, HTTPStatus.BAD_REQUEST),
        ('expMonth', 1, HTTPStatus.CREATED)
    ])
    def test_add_new_card_invalid_data(self, raw_api_client, headers_with_auth, field, value, expected):

        card = prepare_raw_card_payload()

        card[field] = value

        response = raw_api_client.post(
            endpoint='credit_card',
            data=card,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to add new card with missing fields')
    @pytest.mark.parametrize('missing_field, expected', [
        ('fullName', HTTPStatus.BAD_REQUEST),
        ('cardNum', HTTPStatus.BAD_REQUEST),
        ('expYear', HTTPStatus.BAD_REQUEST),
        ('expMonth', HTTPStatus.BAD_REQUEST)
    ])

    def test_add_new_card_missing_fields(self, raw_api_client, headers_with_auth, missing_field, expected):

        card = prepare_raw_card_payload()

        card.pop(missing_field)

        response = raw_api_client.post(
            endpoint='credit_card',
            data=card,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to add new card with wrong HTTP method')
    def test_add_new_card_wrong_method(self, raw_api_client, headers_with_auth):

        card = prepare_raw_card_payload()

        response = raw_api_client.get(
            endpoint='credit_card',
            params=card,
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.METHOD_NOT_ALLOWED)

    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [400, 415, 500]),
        ('Authorization', [401])
    ])
    @allure.title('User not able to add new card with missing headers')
    def test_add_new_card_missing_headers(self, raw_api_client, headers_with_auth, missing_header, codes):

        card = prepare_raw_card_payload()

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header=missing_header
        )

        response = raw_api_client.post_with_raw_headers(
            endpoint='credit_card',
            data=card,
            headers=bad_headers
        )

        assert_status_code_among_expected(response, codes)