from http import HTTPStatus
import allure

from data.constants import DELIVERY_OPTIONS
from utils.assertions.base_assertions import assert_status_code
from utils.assertions.login_assertions import assert_login
from utils.helper import register_user_and_set_security_answer, get_ids_of_products
from utils.schemas.login_request_schema import LoginRequestSchema
from utils.schemas.login_response_schema import LoginResponseSchema
from utils.validators import validate_response


@allure.feature('Login')
@allure.story('Valid login flow')
@allure.title('Registered user able to log in')
class TestLogin:

    def test_registered_user_able_to_log_in(self, register, login):
        _, new_user = register_user_and_set_security_answer(register)

        login_payload = LoginRequestSchema(
            email=new_user.email,
            password=new_user.password
        )

        response = login.log_in_user(
            login_payload
        )

        assert_status_code(response, HTTPStatus.OK)

        validated_response = validate_response(LoginResponseSchema, response.json())

        assert_login(validated_response, login_payload)

    # def test_get_delivery_options(self, delivery_options, headers_with_auth):
    #
    #     resp = delivery_options.get_delivery_options(
    #         headers=headers_with_auth
    #     )
    #     delivery_options = []
    #
    #     for option in resp.json()['data']:
    #         delivery_options.append(option)
    #
    #     with open(r'C:\Users\user\PycharmProjects\PythonProject12\data\constants2.py', 'a', encoding='utf-8') as f:
    #         f.write(f'DELIVERY OPTIONS = {delivery_options}')
    #
    #     print('DONE')