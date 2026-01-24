from http import HTTPStatus

import allure
import pytest

from data.constants import ADDRESS_DELETED_TEXT
from utils.assertions.address_assertions import assert_address_can_be_changed, assert_address_can_be_deleted, \
    assert_num_of_addresses_on_page_matches_expected
from utils.assertions.base_assertions import assert_status_code
from utils.helper import add_address_payload
from utils.schemas.add_address_resp_schema import AddAddressRespSchema, DeleteAddressRespSchema
from utils.validators import validate_response


@allure.feature('Address')
@allure.story('Valid saved address flow')
class TestMySavedAddresses:

    @pytest.mark.delete_address
    @allure.title('User able to change address in my saved addresses')
    def test_user_able_to_change_address(self, create_address, headers_with_auth, address):

        response = create_address(headers_with_auth).response_raw

        validated_initial_address = validate_response(AddAddressRespSchema, response.json())

        modified_address_payload = add_address_payload()

        modified_address_response = address.change_address(
            headers=headers_with_auth,
            data=modified_address_payload,
            address_id=validated_initial_address.data.id
        )

        validated_modified_address = validate_response(AddAddressRespSchema, modified_address_response.json())

        all_addresses = address.get_addresses(
            headers=headers_with_auth
        )

        assert_address_can_be_changed(all_addresses,
            initial_address=validated_initial_address,
            expected_address=validated_modified_address
        )


    @allure.title('User able to delete address in my saved addresses')
    def test_user_able_to_delete_address(self, create_address, address, headers_with_auth):

        response = create_address(headers_with_auth).response_raw

        validated_initial_address = validate_response(AddAddressRespSchema, response.json())

        resp = address.delete_address(
            address_id=validated_initial_address.data.id,
            headers=headers_with_auth
        )

        response_from_deleted = validate_response(DeleteAddressRespSchema, resp.json())

        assert_status_code(resp, HTTPStatus.OK)
        assert_address_can_be_deleted(response_from_deleted, ADDRESS_DELETED_TEXT)

    @allure.title('Deleted address no longer appears in my saved addresses')
    def test_deleted_address_no_longer_appears_on_page(self, create_address, address, headers_with_auth):

        response = create_address(headers_with_auth).response_raw

        validated_initial_address = validate_response(AddAddressRespSchema, response.json())

        address.delete_address(
            address_id=validated_initial_address.data.id,
            headers=headers_with_auth
        )

        all_addresses = address.get_addresses(
            headers=headers_with_auth
        )

        assert_num_of_addresses_on_page_matches_expected(all_addresses, num_of_addresses=0)




