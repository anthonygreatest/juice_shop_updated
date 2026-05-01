
from http import HTTPStatus

import allure
import pytest
from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import prepare_raw_address_payload


@allure.feature('Address')
@allure.story('Invalid add address flow')
class TestAddAddressNegative:

    @allure.title('User not able to add address with invalid data')
    @pytest.mark.parametrize('field, value, expected', [
        ('fullName', 0, HTTPStatus.BAD_REQUEST),
        ('fullName', True, HTTPStatus.BAD_REQUEST),
        ('fullName', 'Jesse'*100, HTTPStatus.BAD_REQUEST),
        ('fullName', 'a', HTTPStatus.BAD_REQUEST),
        ('country', 'USA'*100, HTTPStatus.BAD_REQUEST),
        ('country', 0, HTTPStatus.BAD_REQUEST),
        ('country', True, HTTPStatus.BAD_REQUEST),
        ('country', 'a', HTTPStatus.BAD_REQUEST),
        ('city', 0, HTTPStatus.BAD_REQUEST),
        ('city', True, HTTPStatus.BAD_REQUEST),
        ('city', 'a', HTTPStatus.BAD_REQUEST),
        ('city', 'Albuquerque'*100, HTTPStatus.BAD_REQUEST),
        ('zipCode', 0, HTTPStatus.BAD_REQUEST),
        ('zipCode', "1"*9, HTTPStatus.BAD_REQUEST),
        ('zipCode', "1"*8, HTTPStatus.BAD_REQUEST),
        ('zipCode', True, HTTPStatus.BAD_REQUEST),
        ('zipCode', -1, HTTPStatus.BAD_REQUEST),
        ('mobileNum', 0, HTTPStatus.BAD_REQUEST),
        ('mobileNum', -1, HTTPStatus.BAD_REQUEST),
        ('mobileNum', 99189986411, HTTPStatus.BAD_REQUEST),
        ('mobileNum', 'abc', HTTPStatus.BAD_REQUEST),
        ('streetAddress', 'a'*161, HTTPStatus.BAD_REQUEST),
        ('streetAddress', 'a'*160, HTTPStatus.CREATED),
        ('streetAddress', 0, HTTPStatus.BAD_REQUEST),
        ('streetAddress', True, HTTPStatus.BAD_REQUEST),
        ('streetAddress', 'a', HTTPStatus.BAD_REQUEST),
        ('state', 'New Mexico'*100, HTTPStatus.BAD_REQUEST),
        ('state', 0, HTTPStatus.BAD_REQUEST),
        ('state', True, HTTPStatus.BAD_REQUEST),
        ('state', 'a', HTTPStatus.BAD_REQUEST)
    ])
    @pytest.mark.delete_address
    def test_add_address_with_invalid_data(self, raw_api_client, field, value, expected, headers_with_auth):

        address_to_add = prepare_raw_address_payload()

        address_to_add[field] = value

        response = raw_api_client.post(
            endpoint='add_address',
            data=address_to_add,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to add address with missing fields')
    @pytest.mark.parametrize('missing_field, expected', [
        ('fullName', HTTPStatus.BAD_REQUEST),
        ('streetAddress', HTTPStatus.BAD_REQUEST),
        ('mobileNum', HTTPStatus.BAD_REQUEST),
        ('zipCode', HTTPStatus.BAD_REQUEST),
        ('country', HTTPStatus.BAD_REQUEST),
        ('city', HTTPStatus.BAD_REQUEST),
        ('state', HTTPStatus.CREATED)
    ])
    @pytest.mark.delete_address
    def test_add_address_missing_fields(self, raw_api_client, headers_with_auth, missing_field, expected):

        address_to_add = prepare_raw_address_payload()

        address_to_add.pop(missing_field)

        response = raw_api_client.post(
            endpoint='add_address',
            data=address_to_add,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to add address with wrong HTTP method')
    @pytest.mark.delete_address
    def test_add_address_wrong_method(self, raw_api_client, headers_with_auth):

        address_to_add = prepare_raw_address_payload()

        response = raw_api_client.get(
            endpoint='add_address',
            params=address_to_add,
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.METHOD_NOT_ALLOWED)

    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [400, 415, 500]),
        ('Authorization', [401])
    ])
    @allure.title('User not able to add address with missing headers')
    def test_add_address_missing_headers(self, raw_api_client, headers_with_auth, missing_header, codes):

        address_to_add = prepare_raw_address_payload()

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header=missing_header
        )

        response = raw_api_client.post_with_raw_headers(
            endpoint='add_address',
            data=address_to_add,
            headers=bad_headers
        )

        assert_status_code_among_expected(response, codes)
