import json
from http import HTTPStatus

import allure
import pytest

from data.endpoints import Endpoints
from data.factory import DataFactory
from modules.base_module import BaseModule
from utils.assertions.base_assertions import assert_status_code_among_expected, assert_status_code
from utils.helper import prepare_missing_headers, add_address_payload
from utils.schemas.add_address_request_schema import AddAddressSchema

@allure.feature('Address')
@allure.story('Invalid saved address flow')
class TestSavedAddressesNegative:

    @allure.title('User not able to see addresses with missing headers')
    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [200]),
        ('Authorization', [401, 500])
    ])
    def test_get_my_addresses_missing_headers(self, raw_api_client, headers_with_auth, missing_header, codes):

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header=missing_header
        )

        response = raw_api_client.get(
            endpoint='add_address',
            headers=bad_headers
        )

        assert_status_code_among_expected(response, codes)

    @allure.title('User not able to change address with missing headers')
    @pytest.mark.delete_address
    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [400, 415, 500, 200]),
        ('Authorization', [401, 500])
    ])
    def test_change_my_address_missing_headers(self, address, create_address, missing_header, codes,
        headers_with_auth):

        existing_address = create_address.added_address

        new_address = add_address_payload()

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header=missing_header
        )

        modified_address = address.change_address(
            headers=bad_headers,
            data=new_address,
            address_id=existing_address.data.id
        )

        assert_status_code_among_expected(modified_address, codes)

    @allure.title('User not able to change nonexistent address')
    @pytest.mark.parametrize('address_id, expected', [
        (0, HTTPStatus.NOT_FOUND),
        ('abc', HTTPStatus.NOT_FOUND)
    ])
    def test_change_my_address_nonexistent_address(self, address, headers_with_auth, address_id, expected):

        new_address = add_address_payload()

        modified_address = address.change_address(
            address_id=address_id,
            headers=headers_with_auth,
            data=new_address,
        )

        assert_status_code(modified_address, expected)

    @allure.title('User not able to delete address with missing headers')
    @pytest.mark.delete_address
    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [200]),
        ('Authorization', [401, 500])
    ])
    def test_delete_address_missing_headers(self, address, headers_with_auth, create_address, missing_header, codes):

        address_id = create_address.added_address.data.id

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header=missing_header
        )

        response = address.delete_address(
            address_id=address_id,
            headers=bad_headers
        )

        assert_status_code_among_expected(response, codes)

    @allure.title('User not able to delete nonexistent address')
    @pytest.mark.parametrize('address_id, expected', [
        (0, HTTPStatus.BAD_REQUEST),
        ('abc', HTTPStatus.BAD_REQUEST)
    ])
    def test_delete_address_nonexistent_address(self, address, headers_with_auth, create_address, address_id, expected):

        resp = address.delete_address(
            address_id=address_id,
            headers=headers_with_auth
        )

        assert_status_code(resp, expected)