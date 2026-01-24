from http import HTTPStatus

import allure

from tests.conftest import checkout_factory
from utils.assertions.base_assertions import assert_status_code
from utils.assertions.data_export_assertions import assert_export_data_matches_user_data
from utils.helper import fix_data_export_format, choose_data_export_format, prepare_checkout_response


@allure.feature('Data Export')
@allure.story('Valid data export flow')
class TestDataExport:

    @allure.title('Checking user able to export their data')
    def test_user_able_to_export_data(self, export_data, export_user_data):

        data_export_response, checkout_response = export_user_data()

        validated_response = fix_data_export_format(data_export_response)

        assert_status_code(data_export_response, HTTPStatus.OK)
        assert_export_data_matches_user_data(validated_response, checkout_response)


    @allure.title('Checking user able to export data again with captcha sent')
    def test_user_able_to_export_data_again_with_captcha(self, export_data, headers_with_auth, export_user_data):

        captcha_ans = export_data.request_captcha(
            headers=headers_with_auth
        )

        data_export_response, checkout_response = export_user_data(captcha_ans.answer)

        validated_response = fix_data_export_format(data_export_response)

        assert_status_code(data_export_response, HTTPStatus.OK)
        assert_export_data_matches_user_data(validated_response, checkout_response)




