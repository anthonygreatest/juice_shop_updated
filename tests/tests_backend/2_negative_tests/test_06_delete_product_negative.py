import random
from http import HTTPStatus

import allure
import pytest
from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import product_added_to_basket, prepare_missing_headers
from utils.schemas.add_to_basket_resp_schema import AddToBasketRespSchema


@allure.feature('Basket')
@allure.story('Invalid delete from basket flow')
class TestDeleteFromBasketNegative:

    @allure.title('User not able to delete nonexistent product from basket')
    def test_delete_from_basket_nonexistent_product(self, basket, headers_with_auth):

        resp_to_delete = basket.delete_product_from_basket(
            order_id=random.randint(1, 1000),
            headers=headers_with_auth
        )

        assert_status_code(resp_to_delete, HTTPStatus.NOT_FOUND)

    @allure.title('User not able to delete product from basket with missing headers')
    def test_delete_from_basket_missing_headers(self, login_response, raw_api_client, basket,
        headers_with_auth):

        data = product_added_to_basket(
            login_response=login_response,
            basket=basket,
            headers_with_auth=headers_with_auth
        )

        bad_headers = prepare_missing_headers(headers_with_auth, 'Authorization')

        resp_to_delete = basket.delete_product_from_basket(
            order_id=data.item.id,
            headers=bad_headers
        )

        assert_status_code(resp_to_delete, HTTPStatus.UNAUTHORIZED)
