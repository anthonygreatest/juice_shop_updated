from http import HTTPStatus

import allure
import pytest
from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import prepare_complaint_message, prepare_missing_headers


@allure.feature('Complaint')
@allure.story('Invalid complaint flow')
class TestComplaintNegative:

    @allure.title('User not able to send complaint with invalid data')
    @pytest.mark.parametrize('field, value, expected', [
        ('UserId', 0, HTTPStatus.INTERNAL_SERVER_ERROR),
        ('UserId', 'abc', HTTPStatus.INTERNAL_SERVER_ERROR),
        ('UserId', True, HTTPStatus.BAD_REQUEST),
        ('UserId', None, HTTPStatus.BAD_REQUEST),
        ('message', 1, HTTPStatus.BAD_REQUEST),
        ('message', 'a'*200, HTTPStatus.BAD_REQUEST),
        ('message', 'a'*160, HTTPStatus.CREATED),
        ('message', True, HTTPStatus.BAD_REQUEST),
        ('message', None, HTTPStatus.BAD_REQUEST)
    ])
    def test_send_complaint_invalid_data(self, raw_api_client, register_response, headers_with_auth, field, value, expected):

        user_id = register_response.data.id

        data = prepare_complaint_message(
            user_id=user_id,
            message_type='complaint'
        )

        data[field] = value

        response = raw_api_client.post(
            endpoint='complaint',
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to send complaint with missing fields')
    @pytest.mark.parametrize('missing_field, expected', [
        ('UserId', HTTPStatus.BAD_REQUEST),
        ('message', HTTPStatus.BAD_REQUEST)
    ])
    def test_send_complaint_missing_fields(self, raw_api_client, headers_with_auth, register_response, missing_field, expected):

        user_id = register_response.data.id

        data = prepare_complaint_message(
            user_id=user_id,
            message_type='complaint'
        )

        data.pop(missing_field)

        response = raw_api_client.post(
            endpoint='complaint',
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to send complaint with wrong HTTP method')
    def test_send_complaint_wrong_method(self, raw_api_client, headers_with_auth, register_response):

        user_id = register_response.data.id

        data = prepare_complaint_message(
            user_id=user_id,
            message_type='complaint'
        )

        response = raw_api_client.get(
            endpoint='complaint',
            params=data,
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.METHOD_NOT_ALLOWED)

    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [200, 201]),
        ('Authorization', [401, 500])
    ])
    @allure.title('User not able to send complaint with missing headers')
    def test_send_complaint_missing_auth(self, raw_api_client, headers_with_auth, register_response, missing_header, codes):
        user_id = register_response.data.id

        data = prepare_complaint_message(
            user_id=user_id,
            message_type='complaint'
        )

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header=missing_header
        )

        response = raw_api_client.post(
            endpoint='complaint',
            data=data,
            headers=bad_headers
        )

        assert_status_code_among_expected(response, codes)

