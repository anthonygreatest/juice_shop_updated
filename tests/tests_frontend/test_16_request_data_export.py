from decimal import Decimal

import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from tests.tests_frontend.frontend_helpers import compile_list_of_orders, get_captcha_text
from utils.assertions.data_export_assertions import check_exported_data_matches_user_data


@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.delete_address
@pytest.mark.delete_card
@allure.feature('Request Data Export')
@allure.story('Valid request data export flow')
class TestRequestDataExport:

    @allure.title('Exported email and orders match original data')
    def test_exported_email_and_orders_match_original_data(self, request_data_export_page, order_for_data_export):

        request_data_export_page.open(PlaywrightEndpoints.DATA_EXPORT)

        exported_user_data = request_data_export_page.request_data_export_without_captcha()

        all_orders_by_user = compile_list_of_orders(exported_user_data)

        check_exported_data_matches_user_data(
            exported_data=all_orders_by_user,
            expected_user_data=order_for_data_export
        )

    @allure.title('Captcha can be sent and data is exported')
    def test_request_data_export_captcha_can_be_sent(self, order_for_data_export, request_data_export_page):

        request_data_export_page.open(PlaywrightEndpoints.DATA_EXPORT)

        captcha_answer = get_captcha_text(
            request_data_export_page=request_data_export_page
        )

        exported_data = request_data_export_page.request_data_export(
            captcha_answer
        )

        all_orders_by_user = compile_list_of_orders(exported_data)

        check_exported_data_matches_user_data(
            exported_data=all_orders_by_user,
            expected_user_data=order_for_data_export
        )

