from http import HTTPStatus

import allure
import pytest

from utils.assertions.base_assertions import assert_status_code_among_expected
from utils.helper import fake_data_generator, prepare_login_payload

fake = fake_data_generator()

@allure.feature('Login')
@allure.story('Invalid login flow')
class TestLoginNegative:

    @allure.title('User not able log in with wrong data')
    @pytest.mark.parametrize('email, pwd, expected', [
        (fake.email(), 0, HTTPStatus.UNAUTHORIZED),
        (123, 12345, HTTPStatus.INTERNAL_SERVER_ERROR)
    ])
    def test_login_with_invalid_data(self, raw_api_client, email, pwd, expected):

        data = prepare_login_payload(
            email=email,
            password=pwd
        )

        response = raw_api_client.post(
            endpoint='login',
            data=data
        )

        assert response.status_code == expected

    @allure.title('User not able to log in with wrong HTTP method')
    def test_login_wrong_method(self, raw_api_client, registered_user_data):

        params = prepare_login_payload(
            email=registered_user_data.email,
            password=registered_user_data.password
        )

        resp = raw_api_client.get(
            endpoint='login',
            params=params
        )

        assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


    @allure.title('Login fields protected from SQL injections')
    @pytest.mark.parametrize(
        'input_data', [
            "'; DROP TABLE users; --",
            "/*",
            "abc' OR '1'='1",
            "\" OR \"\"=\"",
            "<script>alert(1)</script>"
        ]
    )
    #если возвращает 500, то значит sql injection доступна
    def test_sql_injection_in_login(self, raw_api_client, registered_user_data, input_data):
        expected = [200, 400, 404]

        params = prepare_login_payload(
            email=registered_user_data.email,
            password=input_data
        )

        resp = raw_api_client.get(
            endpoint='login',
            params=params
        )

        assert_status_code_among_expected(resp, expected)