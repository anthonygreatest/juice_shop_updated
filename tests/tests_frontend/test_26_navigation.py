import allure
import pytest
from playwright.sync_api import expect

from data.frontend_endpoints import PlaywrightEndpoints
from data.locators.all_products_locators import AllProductsLocators
from tests.tests_frontend.frontend_helpers import get_items_per_page
from utils.assertions.search_page_assertions import assert_num_of_items_on_page_matches_expected


@allure.feature('Navigation')
@allure.story('Valid navigation flow')
@allure.title('User can navigate to menu sections')
@pytest.mark.parametrize('section, subsection, expected_url', [
    (AllProductsLocators.orders_and_payment, AllProductsLocators.order_history, PlaywrightEndpoints.ORDER_HISTORY),
    (AllProductsLocators.orders_and_payment, AllProductsLocators.recycle, PlaywrightEndpoints.RECYCLE),
    (AllProductsLocators.orders_and_payment, AllProductsLocators.my_saved_addresses, PlaywrightEndpoints.SAVED_ADDRESSES),
    (AllProductsLocators.orders_and_payment, AllProductsLocators.my_payment_options, PlaywrightEndpoints.SAVED_CARDS),
    (AllProductsLocators.orders_and_payment, AllProductsLocators.digital_wallet, PlaywrightEndpoints.DIGITAL_WALLET),
    (AllProductsLocators.privacy_and_security, AllProductsLocators.privacy_policy, PlaywrightEndpoints.PRIVACY_POLICY),
    (AllProductsLocators.privacy_and_security, AllProductsLocators.request_data_export, PlaywrightEndpoints.DATA_EXPORT),
    (AllProductsLocators.privacy_and_security, AllProductsLocators.request_data_erasure, PlaywrightEndpoints.DATA_ERASURE),
    (AllProductsLocators.privacy_and_security, AllProductsLocators.change_password, PlaywrightEndpoints.CHANGE_PASSWORD_IN_ACCOUNT),
    (AllProductsLocators.privacy_and_security, AllProductsLocators.last_login_ip, PlaywrightEndpoints.LAST_LOGIN_IP),
    (AllProductsLocators.privacy_and_security, AllProductsLocators.two_fa_configuration, PlaywrightEndpoints.TWO_FA_CONFIGURATION)
])
def test_account_menu_sections_can_be_navigated_to(search_page, section, subsection, expected_url):

    search_page.open(PlaywrightEndpoints.ALL_PRODUCTS)

    search_page.go_to_account_section(
        section,
        subsection
    )

    search_page.check_current_url(
        expected_url=expected_url
    )

@allure.feature('Navigation')
@allure.story('Valid navigation flow')
@allure.title('User can access links to sidebar menu sections')
@pytest.mark.parametrize('section, expected_url', [
    (AllProductsLocators.customer_feedback, PlaywrightEndpoints.CUSTOMER_FEEDBACK),
    (AllProductsLocators.complaint, PlaywrightEndpoints.COMPLAINTS),
    (AllProductsLocators.support_chat, PlaywrightEndpoints.CHATBOT),
    (AllProductsLocators.about_us, PlaywrightEndpoints.ABOUT_US),
    (AllProductsLocators.photo_wall, PlaywrightEndpoints.PHOTO_WALL),
    (AllProductsLocators.deluxe_membership, PlaywrightEndpoints.DELUXE_MEMBERSHIP)
])
def test_sidebar_menu_sections_can_be_navigated_to(search_page, section, expected_url):

    search_page.open(PlaywrightEndpoints.ALL_PRODUCTS)

    search_page.go_to_menu_section(
        section
    )

    search_page.check_current_url(
        expected_url=expected_url
    )

@allure.feature('Navigation')
@allure.story('Valid navigation flow')
@allure.title('User can choose to see more items per page')
@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.parametrize('items_per_page', [
    12, 24, 36
])
def test_pagination_dropdown_shows_more_items_per_page(items_per_page, search_page):

    search_page.open(PlaywrightEndpoints.ALL_PRODUCTS)
    search_page.show_more_items_on_page(items_per_page)

    num_of_items = search_page.count_products_on_page()

    assert_num_of_items_on_page_matches_expected(
        actual_items_num=num_of_items,
        expected_items_num=items_per_page
    )

@allure.feature('Navigation')
@allure.story('Valid navigation flow')
@allure.title('User can navigate to different pages and see other items')
@pytest.mark.usefixtures('close_cookies_banner')
def test_pagination_arrows_lead_to_different_pages(search_page):

    search_page.reload()
    search_page.go_to_next_page()
    second_page_info = get_items_per_page(page_num=2, total_pages=3, search_page=search_page)

    search_page.check_page_number_matches_expected(
        expected_page_number=second_page_info
    )

    search_page.go_to_previous_page()
    first_page_info = get_items_per_page(page_num=1, total_pages=3, search_page=search_page)

    search_page.check_page_number_matches_expected(
        expected_page_number=first_page_info
    )



