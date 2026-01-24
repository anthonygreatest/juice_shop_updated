from http import HTTPStatus
import allure
import pytest

from utils.assertions.base_assertions import assert_status_code
from utils.helper import prepare_missing_headers, raw_chatbot_query


@allure.feature('Chat Robot')
@allure.story('Invalid chat robot flow')
class TestChatRobotNegative:

    @allure.title('User not able to ask robot with missing headers')
    def test_ask_robot_missing_headers(self, raw_api_client, headers_with_auth):

        data = raw_chatbot_query()

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header='Authorization'
        )

        response = raw_api_client.post_with_raw_headers(
            endpoint='robot',
            data=data,
            headers=bad_headers
        )

        assert_status_code(response, HTTPStatus.BAD_REQUEST)

    @pytest.mark.skip
    @allure.title('User not able to ask robot with missing fields')
    @pytest.mark.parametrize('field, expected', [
        ('action', HTTPStatus.BAD_REQUEST),
        ('query', HTTPStatus.BAD_REQUEST)
    ])
    def test_ask_robot_missing_fields(self, raw_api_client, headers_with_auth, field, expected):

        data = raw_chatbot_query()

        data.pop(field)

        response = raw_api_client.post(
            endpoint='robot',
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to ask robot with wrong HTTP method')
    def test_ask_robot_wrong_method(self, raw_api_client, headers_with_auth):

        params = raw_chatbot_query()

        response = raw_api_client.get(
            endpoint='robot',
            params=params,
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.INTERNAL_SERVER_ERROR)


