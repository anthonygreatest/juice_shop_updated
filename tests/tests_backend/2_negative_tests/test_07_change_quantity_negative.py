from http import HTTPStatus

import allure
import pytest
from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import product_added_to_basket, prepare_change_quantity_payload, prepare_missing_headers, \
    find_product_limit_per_user


@allure.feature('Basket')
@allure.story('Invalid change quantity flow')
class TestChangeQuantityInBasketNegative:

    @allure.title('User not able to change quantity with invalid data')
    @pytest.mark.parametrize('quantity, expected', [
        (1000, HTTPStatus.BAD_REQUEST),
        (-1000, HTTPStatus.BAD_REQUEST),
        (0, HTTPStatus.BAD_REQUEST),
        ('abc', HTTPStatus.BAD_REQUEST),
        ('', HTTPStatus.BAD_REQUEST),
        (True, HTTPStatus.BAD_REQUEST),
        (1.5, HTTPStatus.BAD_REQUEST),
        (1, HTTPStatus.OK),
    ])
    def test_change_quantity_invalid_data(self, login_response, basket, headers_with_auth, quantity, expected):

        data = product_added_to_basket(
            login_response=login_response,
            basket=basket,
            headers_with_auth=headers_with_auth
        )

        data_to_send = prepare_change_quantity_payload(quantity)

        resp_after_added_one = basket.change_product_quantity(
            order_id=data.item.id,
            data=data_to_send,
            headers=headers_with_auth
        )

        assert_status_code(resp_after_added_one, expected)

    @allure.title('User not able to change quantity above limit per user')
    def test_change_quantity_above_limit_per_user(self, basket, login_response, headers_with_auth):

        data = product_added_to_basket(
            login_response=login_response,
            basket=basket,
            headers_with_auth=headers_with_auth
        )

        limit = find_product_limit_per_user(product_id=data.item.product_id)

        data_to_send = prepare_change_quantity_payload(limit + 1)

        resp_after_added_one = basket.change_product_quantity(
            order_id=data.item.id,
            data=data_to_send,
            headers=headers_with_auth
        )

        assert_status_code(resp_after_added_one, HTTPStatus.BAD_REQUEST)

    @allure.title('User not able to change quantity with wrong HTTP method')
    def test_change_quantity_wrong_method(self, login_response, basket, raw_api_client, headers_with_auth):

        data = product_added_to_basket(
            login_response=login_response,
            basket=basket,
            headers_with_auth=headers_with_auth
        )

        data_to_send = prepare_change_quantity_payload(data.item.quantity + 1)

        resp_after_added_one = raw_api_client.put_with_id(
            endpoint='add_to_basket',
            endpoint_id=data.item.id,
            data=data_to_send,
            headers=headers_with_auth
        )

        assert_status_code(resp_after_added_one, HTTPStatus.METHOD_NOT_ALLOWED)

    @allure.title('User not able to change quantity with missing headers')
    def test_change_quantity_missing_headers(self, headers_with_auth, basket, login_response):

        data = product_added_to_basket(
            login_response=login_response,
            basket=basket,
            headers_with_auth=headers_with_auth
        )

        data_to_send = prepare_change_quantity_payload(data.item.quantity + 1)

        bad_headers = prepare_missing_headers(headers_with_auth, 'Authorization')

        resp_after_added_one = basket.change_product_quantity(
            order_id=data.item.id,
            data=data_to_send,
            headers=bad_headers
        )

        assert_status_code(resp_after_added_one, HTTPStatus.UNAUTHORIZED)