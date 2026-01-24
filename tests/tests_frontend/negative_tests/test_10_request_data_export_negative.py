import allure
import pytest
from data.frontend_endpoints import PlaywrightEndpoints


@pytest.mark.screenshot
@allure.feature('Request Data Export')
@allure.story('Invalid request data export flow')
@pytest.mark.usefixtures('close_cookies_banner')
class TestRequestDataExportNegative:

    @allure.title('User not able to request data export without format selected')
    def test_request_data_export_without_format_selected(self, request_data_export_page):

        request_data_export_page.open(PlaywrightEndpoints.DATA_EXPORT)
        request_data_export_page.check_request_button_remains_disabled()

    @allure.title('User not able to request data export with wrong captcha')
    def test_request_data_export_with_wrong_captcha(self, request_data_export_page):

        captcha = '11111'

        request_data_export_page.open(PlaywrightEndpoints.DATA_EXPORT)
        request_data_export_page.request_data_export_without_captcha()

        request_data_export_page.select_export_format_and_fill_in_captcha(captcha)
        request_data_export_page.click_request()

        request_data_export_page.check_invalid_captcha_error_appears_on_page()

