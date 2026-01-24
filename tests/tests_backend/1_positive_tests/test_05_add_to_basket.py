from http import HTTPStatus

import allure
import pytest

from utils.assertions.base_assertions import assert_status_code
from utils.assertions.basket_assertions import assert_product_added_to_basket, assert_added_product_appears_among_others_in_basket
from utils.schemas.add_to_basket_resp_schema import AddToBasketRespSchema
from utils.validators import validate_response



@allure.feature('Basket')
@allure.story('Valid add to basket flow')
@pytest.mark.delete_product
class TestAddProductToBasket:

    @allure.title('User able to add product into basket')
    def test_product_gets_added_to_basket_successfully(self, add_product_to_basket, login_response, headers_with_auth):

        data = add_product_to_basket(headers_with_auth, login_response)
        response = data.raw_response
        product_to_be_added = data.added_product

        formatted_response = validate_response(AddToBasketRespSchema, response.json())

        assert_status_code(response, HTTPStatus.OK)

        assert_product_added_to_basket(formatted_response, product_to_be_added)

    @allure.title('Added product appears among others in basket')
    def test_added_product_appears_in_basket(self, headers_with_auth, login_response, add_product_to_basket, basket):

        data = add_product_to_basket(headers_with_auth, login_response)
        response = data.raw_response

        formatted_response = validate_response(AddToBasketRespSchema, response.json())

        all_products_in_basket = basket.get_all_products_in_basket(
            order_id=login_response.authentication.bid,
            headers=headers_with_auth
        )

        assert_added_product_appears_among_others_in_basket(all_products_in_basket, formatted_response)

