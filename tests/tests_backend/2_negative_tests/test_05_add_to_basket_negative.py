from http import HTTPStatus

import allure
import pytest
from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import prepare_missing_headers, prepare_raw_add_to_basket_payload


@allure.feature('Basket')
@allure.story('Invalid add to basket flow')
class TestAddToBasketNegative:

    @allure.title('User not able to add product with invalid data')
    @pytest.mark.parametrize('product_id, quantity, expected', [
        (0, 1, HTTPStatus.INTERNAL_SERVER_ERROR),
        (1, 1, HTTPStatus.OK),
        (1, 6, HTTPStatus.BAD_REQUEST),
        (1, -10, HTTPStatus.INTERNAL_SERVER_ERROR),
        (1, 0, HTTPStatus.INTERNAL_SERVER_ERROR),
        (1, 'abc', HTTPStatus.BAD_REQUEST),
        ('abc', 1, HTTPStatus.INTERNAL_SERVER_ERROR),
        (True, 1, HTTPStatus.INTERNAL_SERVER_ERROR),
        (1, True, HTTPStatus.INTERNAL_SERVER_ERROR)
    ])
    def test_add_product_with_invalid_data(self, raw_api_client, login_response,
        headers_with_auth, product_id, quantity, expected):

        data = prepare_raw_add_to_basket_payload(
            bid=login_response.authentication.bid,
            product_id=product_id,
            quantity=quantity
        )

        response = raw_api_client.post(
            endpoint='add_to_basket',
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to add product to nonexistent basket')
    @pytest.mark.parametrize('basket, expected', [
        (-1, HTTPStatus.UNAUTHORIZED),
        ('abc', HTTPStatus.UNAUTHORIZED),
        (0, HTTPStatus.INTERNAL_SERVER_ERROR)
    ])
    def test_add_nonexistent_basket(self, raw_api_client, headers_with_auth, login_response, basket, expected):

        data = prepare_raw_add_to_basket_payload(
            bid=basket,
        )

        response = raw_api_client.post(
            endpoint='add_to_basket',
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to add product with missing fields')
    @pytest.mark.parametrize('missing_field, expected', [
        ('ProductId', HTTPStatus.INTERNAL_SERVER_ERROR),
        ('quantity', HTTPStatus.BAD_REQUEST),
        ('BasketId', HTTPStatus.UNAUTHORIZED)
    ])
    def test_add_product_missing_fields(self, raw_api_client, headers_with_auth, login_response, missing_field, expected):

        data = prepare_raw_add_to_basket_payload(
            bid=login_response.authentication.bid,
        )

        data.pop(missing_field)

        response = raw_api_client.post(
            endpoint='add_to_basket',
            data=data,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to add product with wrong HTTP method')
    def test_add_product_wrong_method(self, raw_api_client, headers_with_auth, login_response):

        params = prepare_raw_add_to_basket_payload(
            bid=login_response.authentication.bid,
        )

        response = raw_api_client.get(
            endpoint='add_to_basket',
            params=params,
            headers=headers_with_auth
        )

        assert_status_code(response, HTTPStatus.METHOD_NOT_ALLOWED)

    @allure.title('User not able to add product with missing headers')
    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [400, 415, 500]),
        ('Authorization', [401])
    ])
    def test_add_product_headers_missing(self, raw_api_client, headers_with_auth, login_response, missing_header, codes):

        data = prepare_raw_add_to_basket_payload(
            bid=login_response.authentication.bid,
        )

        bad_headers = prepare_missing_headers(headers_with_auth, missing_header)

        response = raw_api_client.post_with_raw_headers(
            endpoint='add_to_basket',
            data=data,
            headers=bad_headers
        )

        assert_status_code_among_expected(response, codes)