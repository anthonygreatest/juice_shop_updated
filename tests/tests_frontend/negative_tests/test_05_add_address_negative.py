import json

import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from pages.address_page import AddressPage
from utils.helper import add_address_basic_data


@pytest.mark.screenshot
@allure.feature('Address')
@allure.story('Invalid address flow')
@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.delete_address
class TestAddAddressNegative:

    @allure.title('User not able to add address with empty fields')
    @pytest.mark.parametrize('missing_field, expected_error', [
        ('country', AddressPage.EMPTY_COUNTRY),
        ('full_name', AddressPage.EMPTY_NAME),
        ('mobile_num', AddressPage.EMPTY_MOBILE_NUM),
        ('zip_code', AddressPage.EMPTY_ZIP_CODE),
        ('street_address', AddressPage.EMPTY_ADDRESS),
        ('city', AddressPage.EMPTY_CITY)
    ])
    def test_add_address_with_empty_fields(self, address_page, missing_field, expected_error):

        created_address = add_address_basic_data()
        created_address.pop(missing_field)

        address_page.open(PlaywrightEndpoints.ADD_ADDRESS)
        address_page.reload()
        address_page.address_form.fill(
            **created_address
        )

        address_page.address_form.leave_field_empty(missing_field)

        address_page.check_submit_button_remains_disabled()
        address_page.check_empty_field_error_appears_on_page(expected_error=expected_error)


    @allure.title('User not able to add address with invalid phone number')
    @pytest.mark.parametrize('field, value', [
        ('mobile_num', 791766),
        ('mobile_num', 79176655510),
        ('mobile_num', 791766),
    ])
    def test_add_address_with_invalid_mobile_num(self, address_page, field, value):

        invalid_address = add_address_basic_data()
        invalid_address[field] = value

        address_page.open(PlaywrightEndpoints.ADD_ADDRESS)
        address_page.reload()
        address_page.address_form.fill(
            **invalid_address
        )

        address_page.check_submit_button_remains_disabled()
        address_page.check_invalid_mobile_num_error_appears_on_page()

    @allure.title('User not able to add address with invalid zip code')
    def test_add_address_with_invalid_zip_code_number(self, address_page):

        invalid_address = add_address_basic_data()
        invalid_address['zip_code'] = 123456789

        address_page.open(PlaywrightEndpoints.ADD_ADDRESS)
        address_page.address_form.fill(
            **invalid_address
        )

        address_page.check_submit_button_remains_disabled()
        address_page.check_field_value_not_valid('zip_code')

    @allure.title('User not able to proceed without address selected')
    def test_user_not_able_to_proceed_without_address_selected(self, search_page,
    get_headers, create_address, select_address_page):

        create_address(headers=get_headers)

        select_address_page.open(PlaywrightEndpoints.SELECT_ADDRESS)
        select_address_page.check_continue_to_delivery_button_remains_disabled()

    @pytest.mark.delete_product
    @allure.title('User not able to proceed without delivery option selected')
    def test_user_not_able_to_proceed_without_delivery_option_selected(self,
        add_product_to_basket, basket_id, create_address, select_address_page, get_headers, delivery_options_page):

        add_product_to_basket(
            headers=get_headers,
            login_response=basket_id
        )
        create_address(headers=get_headers)

        select_address_page.open(PlaywrightEndpoints.SELECT_ADDRESS)
        select_address_page.select_address_and_continue()

        delivery_options_page.check_continue_to_payment_button_remains_disabled()

