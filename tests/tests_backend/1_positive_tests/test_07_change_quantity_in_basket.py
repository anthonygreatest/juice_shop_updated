from http import HTTPStatus

import allure
import pytest

from utils.assertions.base_assertions import assert_status_code
from utils.assertions.basket_assertions import assert_product_quantity_in_basket
from utils.helper import change_current_quantity
from utils.schemas.add_to_basket_resp_schema import AddToBasketRespSchema
from utils.validators import validate_response

@pytest.mark.delete_product
@allure.feature('Basket')
@allure.story('Valid add in basket flow')
class TestChangeProductQuantityInBasket:

    @allure.title('Adding (+1) to a product in basket')
    def test_add_in_basket(self, login_response, basket,
        headers_with_auth, add_product_to_basket):

        data = add_product_to_basket(headers_with_auth, login_response)
        added_product = data.item

        new_quantity = change_current_quantity(
            current_quantity=added_product.quantity,
            operation='add',
            number=1
        )

        resp_after_added_one = basket.change_product_quantity(
            order_id=added_product.id,
            data=new_quantity,
            headers=headers_with_auth
        )

        formatted_response = validate_response(AddToBasketRespSchema, resp_after_added_one.json())

        assert_status_code(resp_after_added_one, HTTPStatus.OK)

        assert_product_quantity_in_basket(
            actual_quantity=formatted_response.data.quantity - 1,
            quantity_expected=added_product.quantity
        )


    @allure.title('Removing (-1) from a product in basket')
    def test_remove_from_basket(self, login_response, basket,
        headers_with_auth, add_product_to_basket):

        data = add_product_to_basket(headers_with_auth, login_response)
        added_product = data.item

        new_quantity = change_current_quantity(
            current_quantity=added_product.quantity,
            operation='add',
            number=1
        )

        basket.change_product_quantity(
            order_id=added_product.id,
            data=new_quantity,
            headers=headers_with_auth
        )

        changed_quantity = change_current_quantity(
            current_quantity=added_product.quantity,
            operation='sub',
            number=1
        )

        resp_after_removed_one = basket.change_product_quantity(
            order_id=added_product.id,
            data=changed_quantity,
            headers=headers_with_auth
        )

        formatted_response = validate_response(AddToBasketRespSchema, resp_after_removed_one.json())

        assert_status_code(resp_after_removed_one, HTTPStatus.OK)

        assert_product_quantity_in_basket(
            actual_quantity=formatted_response.data.quantity + 1,
            quantity_expected=added_product.quantity
        )


