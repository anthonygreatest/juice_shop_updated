import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from utils.helper import add_address_payload, add_address_basic_data


@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.delete_address
@allure.feature('Address')
@allure.story('Valid add address flow')
class TestAddAddress:

    @allure.title('Added address appears on select address page')
    def test_added_new_address_appears_on_page(self, select_address_page, address_page, add_new_address):

        select_address_page.open(PlaywrightEndpoints.SELECT_ADDRESS)
        select_address_page.click_add_new_address()

        address_data = add_address_basic_data()
        add_new_address(address_page, address_data)

        select_address_page.check_address_matches_expected(
            expected_data=address_data
        )

    @allure.title('Added address success toast appears on page')
    def test_added_new_address_toast(self, add_new_address, address_page, select_address_page):
        select_address_page.open(PlaywrightEndpoints.SELECT_ADDRESS)
        select_address_page.click_add_new_address()

        address_data = add_address_basic_data()
        add_new_address(address_page, address_data)

        select_address_page.check_address_added_toast_appears_on_page(
            city=address_data.city
        )


    @allure.title('Added address appears on delivery page')
    def test_address_appears_on_delivery_page(self, select_address_page, get_headers, create_address, delivery_options_page):

        address_data = create_address(
            headers=get_headers
        ).address_payload

        select_address_page.open(PlaywrightEndpoints.SELECT_ADDRESS)
        select_address_page.select_address_and_continue()

        delivery_options_page.check_delivery_info_matches_expected(
            delivery_data=address_data
        )


