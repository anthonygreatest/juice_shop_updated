from http import HTTPStatus

import allure
import pytest
from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import prepare_missing_headers, prepare_recycle_payload_for_invalid_data


@allure.feature('Recycle')
@allure.story('Invalid recycle flow')
class TestRecycleNegative:

    @allure.title('User not able to recycle with invalid data')
    @pytest.mark.parametrize('field, value, pickup, expected', [
        ('UserId', 0, False, HTTPStatus.BAD_REQUEST),
        ('UserId', True, False, HTTPStatus.BAD_REQUEST),
        ('UserId', 'abc', False, HTTPStatus.BAD_REQUEST),
        ('AddressId', 0, False, HTTPStatus.BAD_REQUEST),
        ('AddressId', True, False, HTTPStatus.BAD_REQUEST),
        ('AddressId', 'abc', False, HTTPStatus.BAD_REQUEST),
        ('quantity', 0, False, HTTPStatus.BAD_REQUEST),
        ('quantity', True, False, HTTPStatus.BAD_REQUEST),
        ('quantity', 'abc', False, HTTPStatus.BAD_REQUEST),
        ('quantity', 9, False, HTTPStatus.BAD_REQUEST),
        ('quantity', 10, False, HTTPStatus.CREATED),
        ('quantity', 10, True, HTTPStatus.BAD_REQUEST),
        ('quantity', 101, True, HTTPStatus.CREATED),
        ('quantity', 1001, True, HTTPStatus.BAD_REQUEST),
        ('quantity', -1, False, HTTPStatus.BAD_REQUEST)
    ])
    def test_recycle_invalid_data(self, raw_api_client, headers_with_auth, create_address, field, value, pickup, expected):

        user_id = create_address.added_address.data.user_id
        address_id = create_address.added_address.data.id

        data = prepare_recycle_payload_for_invalid_data(
            user_id=user_id,
            address_id=address_id,
            pickup_needed=pickup
        )

        data[field] = value

        response = raw_api_client.post(
            endpoint='recycle',
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to recycle with missing fields')
    @pytest.mark.parametrize('missing_field, expected', [
        ('UserId', HTTPStatus.BAD_REQUEST),
        ('AddressId', HTTPStatus.BAD_REQUEST),
        ('quantity', HTTPStatus.BAD_REQUEST)
    ])
    def test_recycle_missing_fields(self, raw_api_client, headers_with_auth, create_address, missing_field, expected):
        user_id = create_address.added_address.data.user_id
        address_id = create_address.added_address.data.id

        data = prepare_recycle_payload_for_invalid_data(
            user_id=user_id,
            address_id=address_id
        )

        data.pop(missing_field)

        response = raw_api_client.post(
            endpoint='recycle',
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to recycle with wrong HTTP method')
    def test_recycle_wrong_method(self, raw_api_client, headers_with_auth, create_address):

        user_id = create_address.added_address.data.user_id
        address_id = create_address.added_address.data.id

        params = prepare_recycle_payload_for_invalid_data(
            user_id=user_id,
            address_id=address_id
        )

        response = raw_api_client.get(
            endpoint='recycle',
            params=params,
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.METHOD_NOT_ALLOWED)

    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [200, 201]),
        ('Authorization', [401, 500])
    ])
    @allure.title('User not able to recycle with missing headers')
    def test_recycle_missing_headers(self, raw_api_client, headers_with_auth, create_address, missing_header, codes):

        user_id = create_address.added_address.data.user_id
        address_id = create_address.added_address.data.id

        data = prepare_recycle_payload_for_invalid_data(
            user_id=user_id,
            address_id=address_id
        )

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header=missing_header
        )

        response = raw_api_client.post_with_raw_headers(
            endpoint='recycle',
            data=data,
            headers=bad_headers
        )

        assert_status_code_among_expected(response, codes)

