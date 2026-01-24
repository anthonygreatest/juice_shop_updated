from http import HTTPStatus

import allure
import pytest

from data.factory import DataFactory
from utils.helper import fake_data_generator, register_user_and_set_security_answer, \
    registered_user_with_changed_password, create_invalid_fields, change_password_payload

fake = fake_data_generator()

@allure.feature('Change Password')
@allure.story('Invalid change password flow')
class TestChangePasswordNegative:

    @allure.title('User not able to reset password with wrong security answer')
    @pytest.mark.parametrize('answer, expected', [
        ('', HTTPStatus.INTERNAL_SERVER_ERROR),
        ('good', HTTPStatus.UNAUTHORIZED),
        (None, HTTPStatus.INTERNAL_SERVER_ERROR),
        (True, HTTPStatus.INTERNAL_SERVER_ERROR)
    ])
    def test_reset_password_wrong_security_answer(self, register, answer, expected, raw_api_client):

        body = registered_user_with_changed_password(
            register=register
        )

        new_password_payload = create_invalid_fields(
            invalid_fields=[('answer', answer)],
            data=body
        )

        response = raw_api_client.post(
            endpoint='change_password',
            data=new_password_payload
        )

        assert response.status_code == expected

    @allure.title('Unregistered user not able to reset password')
    def test_reset_password_nonexistent_user(self, raw_api_client, register):

        formatted_response, random_user = register_user_and_set_security_answer(register)

        body = change_password_payload(
            email=fake.email(),
            security_answer=random_user.security_answer
        )

        response = raw_api_client.post(
            endpoint='change_password',
            data=body
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @allure.title('User not able to reset password with invalid password')
    @pytest.mark.parametrize('password, repeat, expected', [
        ('', '', HTTPStatus.UNAUTHORIZED),
        (1, 1, HTTPStatus.INTERNAL_SERVER_ERROR),
        (fake.password(), 0, HTTPStatus.UNAUTHORIZED),
        (True, True, HTTPStatus.INTERNAL_SERVER_ERROR),
        ('tony1806', 'tony1806', HTTPStatus.OK)

    ])
    def test_reset_password_invalid_password(self, raw_api_client, register, password, repeat, expected):

        body = registered_user_with_changed_password(
            register=register
        )

        new_password_payload = create_invalid_fields(
            invalid_fields=[('new', password), ('repeat', repeat)],
            data=body
        )

        response = raw_api_client.post(
            endpoint='change_password',
            data=new_password_payload
        )

        assert response.status_code == expected

    @allure.title('User not able to reset password with missing fields')
    @pytest.mark.parametrize('missing_field, expected', [
        ('email', HTTPStatus.INTERNAL_SERVER_ERROR),
        ('answer', HTTPStatus.INTERNAL_SERVER_ERROR),
        ('new', HTTPStatus.UNAUTHORIZED),
        ('repeat', HTTPStatus.UNAUTHORIZED)
    ])
    def test_reset_password_with_missing_fields(self, raw_api_client, register, missing_field, expected):

        body = registered_user_with_changed_password(
            register=register
        )

        body.pop(missing_field)

        response = raw_api_client.post(
            endpoint='change_password',
            data=body
        )

        assert response.status_code == expected

    @allure.title('User not able to reset password with wrong HTTP method')
    def test_reset_password_wrong_method(self, register, raw_api_client):

        body = registered_user_with_changed_password(
            register=register
        )

        response = raw_api_client.get(
            endpoint='change_password',
            params=body
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
