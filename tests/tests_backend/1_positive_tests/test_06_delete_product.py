from http import HTTPStatus

import allure
from utils.assertions.base_assertions import assert_status_code
from utils.assertions.basket_assertions import assert_deleted_product_no_longer_in_basket, \
    assert_number_of_products_in_basket
from utils.schemas.add_to_basket_resp_schema import ProductInBasketSchema
from utils.validators import validate_response


@allure.feature('Basket')
@allure.story('Valid delete from basket flow')
class TestDeleteProductFromBasket:

    @allure.title('User able to delete product from basket')
    def test_delete_product_gets_deleted(self, basket, headers_with_auth,
        login_response, add_product_to_basket):

        data = add_product_to_basket(headers_with_auth, login_response)
        product_to_delete = data.item

        resp_to_delete = basket.delete_product_from_basket(
            order_id=product_to_delete.id,
            headers=headers_with_auth
        )

        formatted_response = validate_response(ProductInBasketSchema, resp_to_delete.json())

        assert_status_code(resp_to_delete, HTTPStatus.OK)

        assert_deleted_product_no_longer_in_basket(formatted_response, 0)

    @allure.title('Deleted product no longer in basket')
    def test_deleted_product_no_longer_appears_in_basket(self, basket, headers_with_auth,
        login_response, add_product_to_basket):

        data = add_product_to_basket(headers_with_auth, login_response)
        product_to_delete = data.item

        basket.delete_product_from_basket(
            order_id=product_to_delete.id,
            headers=headers_with_auth
        )

        all_products_in_basket = basket.get_all_products_in_basket(
            order_id=login_response.authentication.bid,
            headers=headers_with_auth
        )

        assert_number_of_products_in_basket(all_products_in_basket, 0)