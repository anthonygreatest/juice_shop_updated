import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.add_address_request_schema import AddAddressSchema
from utils.schemas.add_address_resp_schema import AddAddressRespSchema, GetAddressesRespSchema, DeleteAddressRespSchema

logger = get_logger("ADDRESS_ASSERTIONS")

@allure.step('Checking address gets added')
def assert_address_added(response: AddAddressRespSchema, expected: AddAddressSchema):

    logger.info('Checking address gets added')

    assert_match(response.data.full_name, expected.full_name, 'full_name')
    assert_match(response.data.country, expected.country, 'country')
    assert_match(response.data.mobile_num, expected.mobile_num, 'mobile_num')
    assert_match(response.data.zip_code, expected.zip_code, 'zip_code')
    assert_match(response.data.street_address, expected.street_address, 'street_address')
    assert_match(response.data.city, expected.city, 'city')
    assert_match(response.data.state, expected.state, 'state')


@allure.step('Checking address appears among saved')
def assert_added_address_appears_among_saved(response: GetAddressesRespSchema, expected: AddAddressSchema):

    logger.info('Checking product gets added to basket')

    matched_address = next(
        (address for address in response.data if address.full_name == expected.full_name),
        None
    )

    assert matched_address, f'Address with {expected.full_name} not found'

    assert_match(matched_address.full_name, expected.full_name, 'full_name')
    assert_match(matched_address.country, expected.country, 'country')
    assert_match(matched_address.mobile_num, expected.mobile_num, 'mobile_num')
    assert_match(matched_address.zip_code, expected.zip_code, 'zip_code')
    assert_match(matched_address.street_address, expected.street_address, 'street_address')
    assert_match(matched_address.city, expected.city, 'city')
    assert_match(matched_address.state, expected.state, 'state')

@allure.step('Checking address gets changed')
def assert_address_can_be_changed(response: GetAddressesRespSchema,
    initial_address: AddAddressRespSchema, expected_address: AddAddressRespSchema):

    assert expected_address.data in response.data \
           and initial_address.data not in response.data

@allure.step('Checking address gets deleted')
def assert_address_can_be_deleted(response: DeleteAddressRespSchema, expected_text: str):

    assert_match(response.data, expected_text, 'data text')

@allure.step('Checking address gets deleted')
def assert_num_of_addresses_on_page_matches_expected(response: GetAddressesRespSchema, num_of_addresses: int):

    assert_match(len(response.data), num_of_addresses, 'num of addresses')

@allure.step('Checking added address gets deleted')
def check_num_of_addresses_on_page_matches_expected(actual_num: int, expected_num: int):

    assert_match(actual_num, expected_num, 'num of addresses')