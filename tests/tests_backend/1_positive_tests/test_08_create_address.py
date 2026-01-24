from http import HTTPStatus

import allure
import pytest

from utils.assertions.address_assertions import assert_address_added, assert_added_address_appears_among_saved
from utils.assertions.base_assertions import assert_status_code
from utils.schemas.add_address_resp_schema import AddAddressRespSchema
from utils.validators import validate_response


@pytest.mark.delete_address
@allure.feature('Address')
@allure.story('Valid add address flow')
class TestAddress:

    @allure.title('User able to create address successfully')
    def test_user_able_to_create_address(self, create_address, headers_with_auth):

        address_data = create_address(headers_with_auth)

        response = address_data.response_raw
        address_to_be_added = address_data.address_payload

        validated_response = validate_response(AddAddressRespSchema, response.json())

        assert_status_code(response, HTTPStatus.CREATED)

        assert_address_added(validated_response, address_to_be_added)

    @allure.title('Created address gets saved among others')
    def test_created_address_gets_saved_among_others(self, create_address, address, headers_with_auth):
        address_to_be_added = create_address(headers_with_auth).address_payload

        all_addresses = address.get_addresses(
            headers=headers_with_auth
        )

        assert_added_address_appears_among_saved(all_addresses, address_to_be_added)

