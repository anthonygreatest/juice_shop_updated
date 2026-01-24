from http import HTTPStatus

import allure
import pytest
from utils.assertions.base_assertions import assert_status_code
from utils.helper import prepare_raw_customer_feedback_payload, prepare_missing_headers


@allure.feature('Customer Feedback')
@allure.story('Invalid customer feedback flow')
class TestSendFeedbackNegative:

    @allure.title('User not able to send feedback with invalid data')
    @pytest.mark.parametrize('field, value, expected', [
        ('UserId', 0, HTTPStatus.INTERNAL_SERVER_ERROR),
        ('UserId', 'abc', HTTPStatus.INTERNAL_SERVER_ERROR),
        ('UserId', True, HTTPStatus.BAD_REQUEST),
        ('UserId', None, HTTPStatus.BAD_REQUEST),
        ('comment', 1, HTTPStatus.BAD_REQUEST),
        ('comment', 'a' * 200, HTTPStatus.BAD_REQUEST),
        ('comment', 'a' * 160, HTTPStatus.CREATED),
        ('comment', True, HTTPStatus.BAD_REQUEST),
        ('comment', None, HTTPStatus.BAD_REQUEST),
        ('rating', True, HTTPStatus.BAD_REQUEST),
        ('rating', 1, HTTPStatus.CREATED),
        ('rating', 6, HTTPStatus.BAD_REQUEST),
        ('rating', 'abc', HTTPStatus.BAD_REQUEST),
        ('rating', 0, HTTPStatus.BAD_REQUEST),
        ('captcha', 0, HTTPStatus.UNAUTHORIZED),
        ('captchaId', 0, HTTPStatus.UNAUTHORIZED),
    ])
    def test_send_feedback_invalid_data(self, customer_feedback, headers_with_auth, register_response,
        raw_api_client, field, value, expected):

        data = prepare_raw_customer_feedback_payload(
            customer_feedback=customer_feedback,
            headers_with_auth=headers_with_auth,
            user_id=register_response.data.id
        )

        data[field] = value

        response = raw_api_client.post(
            endpoint='feedback',
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to send feedback with missing fields')
    @pytest.mark.parametrize('missing_field, expected', [
        ('UserId', HTTPStatus.BAD_REQUEST),
        ('captcha', HTTPStatus.UNAUTHORIZED),
        ('captchaId', HTTPStatus.INTERNAL_SERVER_ERROR),
        ('comment', HTTPStatus.BAD_REQUEST),
        ('rating', HTTPStatus.BAD_REQUEST)
    ])
    def test_send_feedback_missing_fields(self, headers_with_auth, register_response, customer_feedback,
        raw_api_client, missing_field, expected):

        data = prepare_raw_customer_feedback_payload(
            customer_feedback=customer_feedback,
            headers_with_auth=headers_with_auth,
            user_id=register_response.data.id
        )

        data.pop(missing_field)

        response = raw_api_client.post(
            endpoint='feedback',
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to send feedback with wrong HTTP method')
    def test_send_feedback_wrong_method(self, headers_with_auth, register_response, customer_feedback,
        raw_api_client):

        data = prepare_raw_customer_feedback_payload(
            customer_feedback=customer_feedback,
            headers_with_auth=headers_with_auth,
            user_id=register_response.data.id
        )

        response = raw_api_client.get(
            endpoint='feedback',
            params=data,
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.METHOD_NOT_ALLOWED)

    @allure.title('User not able to send feedback with missing headers')
    @pytest.mark.parametrize('missing_header, expected', [
        ('Content-Type', HTTPStatus.INTERNAL_SERVER_ERROR),
        ('Authorization', HTTPStatus.CREATED)
    ])
    def test_send_feedback_headers_missing(self, headers_with_auth, register_response, customer_feedback,
        raw_api_client, missing_header, expected):

        payload = prepare_raw_customer_feedback_payload(
            customer_feedback=customer_feedback,
            headers_with_auth=headers_with_auth,
            user_id=register_response.data.id
        )

        bad_headers = prepare_missing_headers(headers_with_auth, missing_header)

        response = raw_api_client.post_with_raw_headers(
            endpoint='feedback',
            data=payload,
            headers=bad_headers
        )

        assert_status_code(response, expected)