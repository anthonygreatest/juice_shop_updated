from http import HTTPStatus

import allure
import pytest
from data.constants import SECURITY_QUESTIONS, UNIQUE_EMAIL_ERROR

from data.generators.generator import GenerateLongEmail
from utils.assertions.base_assertions import assert_status_code
from utils.assertions.register_assertions import assert_user_not_able_to_register_again
from utils.helper import generate_password_pair, fake_data_generator, \
    registered_user, prepare_register_payload_for_invalid_data, create_invalid_fields

fake = fake_data_generator()

@allure.feature('User Registration')
@allure.story('Invalid registration flow')
class TestRegisterUserNegative:

    @allure.title('User not registered with invalid data')
    @pytest.mark.parametrize('email, password, repeat_password, expected', [
        (fake.email(), '', '', HTTPStatus.BAD_REQUEST),
        (fake.email(), 1, 1, HTTPStatus.INTERNAL_SERVER_ERROR),
        (fake.email(), True, True, HTTPStatus.INTERNAL_SERVER_ERROR),
        (fake.email(), *generate_password_pair(), HTTPStatus.CREATED),
        ('', *generate_password_pair(), HTTPStatus.BAD_REQUEST),
        (123, *generate_password_pair(), HTTPStatus.INTERNAL_SERVER_ERROR),
        ('@!walter', *generate_password_pair(), HTTPStatus.BAD_REQUEST),
        (GenerateLongEmail().generate_long_email(), *generate_password_pair(), HTTPStatus.BAD_REQUEST),
        ('1', *generate_password_pair(), HTTPStatus.BAD_REQUEST),
        (True, *generate_password_pair(), HTTPStatus.INTERNAL_SERVER_ERROR),
        (fake.email(), fake.password(), 1, HTTPStatus.INTERNAL_SERVER_ERROR),
        (fake.email(), fake.password(), '', HTTPStatus.BAD_REQUEST)
    ])
    def test_register_invalid_user(self, raw_api_client, email, password, repeat_password, expected):

        data = prepare_register_payload_for_invalid_data()

        invalid_payload = create_invalid_fields(invalid_fields=[
            ('email', email),
            ('password', password),
            ('passwordRepeat', repeat_password)],
            data=data
        )

        response = raw_api_client.post(
            endpoint='register',
            data=invalid_payload
        )

        assert_status_code(response, expected)

    @allure.title('User not registered with missing fields')
    @pytest.mark.parametrize('missing_field, expected', [
        ('email', HTTPStatus.INTERNAL_SERVER_ERROR),
        ('password', HTTPStatus.INTERNAL_SERVER_ERROR),
        ('passwordRepeat', HTTPStatus.INTERNAL_SERVER_ERROR),
        ('securityQuestion', HTTPStatus.INTERNAL_SERVER_ERROR),
        ('securityAnswer', HTTPStatus.INTERNAL_SERVER_ERROR),
    ])
    def test_register_with_missing_fields(self, raw_api_client, missing_field, expected):

        data = prepare_register_payload_for_invalid_data()

        data.pop(missing_field)

        response = raw_api_client.post(
            endpoint='register',
            data=data
        )

        assert_status_code(response, expected)

    @allure.title('User not registered with nonexistent security question')
    def test_register_with_nonexistent_security_question(self, raw_api_client):

        data = prepare_register_payload_for_invalid_data()
        data['securityQuestion']['id'] = len(SECURITY_QUESTIONS) + 1
        data['securityQuestion']['question'] = 'Favorite football club?'
        data['securityAnswer'] = 'Chelsea'

        response = raw_api_client.post(
            endpoint='register',
            data=data
        )

        assert_status_code(response, HTTPStatus.BAD_REQUEST)

    @allure.title('Same user not able to register second time')
    def test_register_user_again(self, register):

        formatted_response, new_user = registered_user(register)

        second_registration_response = register.register_new_user(
            data=new_user
        )

        assert_status_code(second_registration_response, HTTPStatus.BAD_REQUEST)
        assert_user_not_able_to_register_again(second_registration_response, UNIQUE_EMAIL_ERROR)

    @allure.title('User not registered with wrong HTTP method')
    def test_register_wrong_method(self, raw_api_client):

        params = prepare_register_payload_for_invalid_data()

        response = raw_api_client.get(
            endpoint='register',
            params=params
        )

        assert_status_code(response, HTTPStatus.UNAUTHORIZED)





