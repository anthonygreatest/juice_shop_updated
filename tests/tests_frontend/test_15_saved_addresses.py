import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from utils.assertions.address_assertions import check_num_of_addresses_on_page_matches_expected
from utils.helper import add_address_payload, add_address_basic_data


@pytest.mark.usefixtures('close_cookies_banner')
@allure.feature('Address')
@allure.story('Valid address flow')
class TestSavedAddresses:

    @pytest.mark.delete_address
    @allure.title('Added address appears on saved addresses page')
    def test_newly_added_address_appears_on_saved_addresses_page(self, saved_addresses_page, create_address, get_headers):

        added_address = create_address(get_headers)

        saved_addresses_page.open(PlaywrightEndpoints.SAVED_ADDRESSES)

        saved_addresses_page.check_address_data_on_saved_addresses_page_matches_expected(
            expected_data=added_address.address_payload
        )

    @allure.title('Deleted address appears on saved addresses page')
    def test_deleted_address_no_longer_appears_on_page(self, create_address, get_headers,
        saved_addresses_page):

        create_address(get_headers)

        saved_addresses_page.open(PlaywrightEndpoints.SAVED_ADDRESSES)
        saved_addresses_page.reload()

        cnt_before = saved_addresses_page.get_num_of_addresses_on_page()

        saved_addresses_page.remove_address()

        cnt_after = saved_addresses_page.get_num_of_addresses_on_page()

        check_num_of_addresses_on_page_matches_expected(
            actual_num=cnt_after,
            expected_num=cnt_before - 1
        )

    @pytest.mark.delete_address
    @allure.title('Edited address appears on saved addresses page')
    def test_edited_address_appears_on_page(self, create_address, saved_addresses_page, get_headers,
        add_new_address):

        create_address(get_headers)

        saved_addresses_page.open(PlaywrightEndpoints.SAVED_ADDRESSES)
        saved_addresses_page.reload()

        new_address_data = add_address_basic_data()

        saved_addresses_page.edit_address()

        add_new_address(
            address_page=saved_addresses_page,
            address_data=new_address_data
        )

        saved_addresses_page.check_address_data_on_saved_addresses_page_matches_expected(
            expected_data=new_address_data
        )

    @pytest.mark.delete_address
    @allure.title('Edited address appears on saved addresses page')
    def test_edited_address_toast_appears_on_page(self, create_address, saved_addresses_page, get_headers,
        add_new_address):

        create_address(get_headers)

        saved_addresses_page.open(PlaywrightEndpoints.SAVED_ADDRESSES)
        saved_addresses_page.reload()

        new_address_data = add_address_basic_data()

        saved_addresses_page.edit_address()

        add_new_address(
            address_page=saved_addresses_page,
            address_data=new_address_data
        )

        saved_addresses_page.check_address_updated_toast_appears_on_page(
            city=new_address_data.city
        )




