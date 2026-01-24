from http import HTTPStatus

import allure
import pytest

from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import choose_data_export_format_raw, prepare_missing_headers


@allure.feature('Data Export')
@allure.story('Invalid data export flow')
class TestDataExportNegative:

    @allure.title('User not able to send complaint with invalid data')
    @pytest.mark.parametrize('field, value, expected', [
        ('option', 0, HTTPStatus.BAD_REQUEST),
        ('option', 'abc', HTTPStatus.BAD_REQUEST),
        ('option', True, HTTPStatus.BAD_REQUEST),
        ('option', None, HTTPStatus.BAD_REQUEST),
        ('answer', 1, HTTPStatus.BAD_REQUEST),
    ])
    def test_data_export_with_invalid_data(self, raw_api_client, headers_with_auth, field, value, expected):

        data = choose_data_export_format_raw()
        data[field] = value

        data_export_response = raw_api_client.post(
            endpoint='data_export',
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(data_export_response, expected)

    @allure.title('User not able to become deluxe member with missing headers')
    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [415, 400, 500, 401]),
        ('Authorization', [401])
    ])
    def test_data_export_with_missing_headers(self, raw_api_client, headers_with_auth, missing_header, codes):
        data = choose_data_export_format_raw()

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header=missing_header
        )

        data_export_response = raw_api_client.post_with_raw_headers(
            endpoint='data_export',
            data=data,
            headers=bad_headers
        )

        assert_status_code_among_expected(data_export_response, codes)

    def test_data_export_with_wrong_method(self, raw_api_client, headers_with_auth):

        params = choose_data_export_format_raw()

        data_export_response = raw_api_client.get(
            endpoint='data_export',
            params=params,
            headers=headers_with_auth
        )

        assert_status_code(data_export_response, HTTPStatus.INTERNAL_SERVER_ERROR)
