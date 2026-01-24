import random
from http import HTTPStatus
import allure
import pytest

from data.constants import PRODUCTS_LIST
from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import prepare_review_to_like, prepare_raw_review_payload, prepare_missing_headers


@allure.feature('Reviews')
@allure.story('Invalid like review flow')
class TestLikeReviewNegative:

    @allure.title('User not able to leave likes under nonexistent comments')
    @pytest.mark.parametrize('comment_id, expected', [
        (1, HTTPStatus.NOT_FOUND),
        ('abc', HTTPStatus.NOT_FOUND),
        ('', HTTPStatus.NOT_FOUND)
    ])
    def test_like_nonexistent_comment(self, headers_with_auth, raw_api_client, comment_id, expected):

        favorite_review = prepare_review_to_like(comment_id)

        response = raw_api_client.post(
            endpoint='reviews',
            data=favorite_review,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to leave likes with missing headers')
    def test_like_comment_with_headers_missing(self, get_unliked_review, raw_api_client):

        comment_to_like = get_unliked_review.comment_to_like

        favorite_review = prepare_review_to_like(comment_to_like)

        response = raw_api_client.post(
            endpoint='reviews',
            data=favorite_review
        )

        assert_status_code(response, HTTPStatus.UNAUTHORIZED)

    @allure.title('User not able leave likes with wrong HTTP method')
    def test_like_comment_wrong_method(self, get_unliked_review, headers_with_auth, raw_api_client):

        comment_to_like = get_unliked_review.comment_to_like

        favorite_review = prepare_review_to_like(comment_to_like)

        response = raw_api_client.get(
            endpoint='reviews',
            params=favorite_review,
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.INTERNAL_SERVER_ERROR)

@allure.feature('Reviews')
@allure.story('Invalid write review flow')
class TestWriteReviewNegative:

    @allure.title('User not able to write review with invalid data')
    @pytest.mark.parametrize('field, value, expected', [
        ('message', 'a' * 200, HTTPStatus.BAD_REQUEST),
        ('message', 'a' * 160, HTTPStatus.CREATED),
        ('message', True, HTTPStatus.BAD_REQUEST),
        ('message', None, HTTPStatus.BAD_REQUEST),
        ('author', '', HTTPStatus.BAD_REQUEST),
        ('author', None, HTTPStatus.BAD_REQUEST),
        ('author', 1, HTTPStatus.BAD_REQUEST),
    ])
    def test_write_review_with_invalid_data(self, raw_api_client, login_response, headers_with_auth, field, value, expected):

        selected_product = random.choice(PRODUCTS_LIST)['id']

        data_to_send = prepare_raw_review_payload(
            email=login_response.authentication.umail
        )

        data_to_send[field] = value

        response = raw_api_client.leave_review(
            endpoint='all_reviews',
            product_id=selected_product,
            data=data_to_send,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to write review with wrong HTTP method')
    def test_write_review_wrong_method(self, raw_api_client, headers_with_auth, login_response):

        selected_product = random.choice(PRODUCTS_LIST)['id']

        data_to_send = prepare_raw_review_payload(
            email=login_response.authentication.umail
        )

        response = raw_api_client.leave_review_invalid_method(
            endpoint='all_reviews',
            endpoint_id=selected_product,
            data=data_to_send,
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.INTERNAL_SERVER_ERROR)

    @allure.title('User not able to write review with missing fields')
    @pytest.mark.parametrize('field, expected', [
            ('message', HTTPStatus.BAD_REQUEST),
            ('author', HTTPStatus.BAD_REQUEST)
    ])
    def test_write_review_with_missing_fields(self, raw_api_client, headers_with_auth,
        login_response, field, expected):

        selected_product = random.choice(PRODUCTS_LIST)['id']

        data_to_send = prepare_raw_review_payload(
            email=login_response.authentication.umail
        )

        data_to_send.pop(field)

        response = raw_api_client.leave_review(
            endpoint='all_reviews',
            product_id=selected_product,
            data=data_to_send,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to write review with missing fields')
    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [415, 400, 500, 401]),
        ('Authorization', [401])
    ])
    def test_write_review_with_missing_headers(self, raw_api_client, headers_with_auth,
        login_response, missing_header, codes):

        selected_product = random.choice(PRODUCTS_LIST)['id']

        data_to_send = prepare_raw_review_payload(
            email=login_response.authentication.umail
        )

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header=missing_header
        )

        response = raw_api_client.put_with_id_with_raw_headers(
            endpoint='all_reviews',
            endpoint_id=selected_product,
            data=data_to_send,
            headers=bad_headers
        )

        assert_status_code_among_expected(response, codes)

