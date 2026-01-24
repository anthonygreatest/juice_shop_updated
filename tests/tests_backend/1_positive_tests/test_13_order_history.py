from http import HTTPStatus

import allure
import pytest
from utils.assertions.base_assertions import assert_status_code
from utils.assertions.order_history_assertions import assert_order_history_matches_order_data
from utils.helper import prepare_checkout_response
from utils.schemas.get_order_history_schema import GetOrderHistoryListSchema
from utils.validators import validate_response


@pytest.mark.delete_address
@pytest.mark.delete_card
@allure.feature('Order History')
@allure.story('Valid order history flow')
@allure.title('Order history matches order data')
def test_order_history_matches_order_data(checkout_factory, order_history, headers_with_auth, login_response):

    checkout_data = checkout_factory(e_wallet=False, headers=headers_with_auth, login_response=login_response)

    checkout_response = prepare_checkout_response(checkout_data)
    selected_product = checkout_data.selected_product
    card_to_be_added = checkout_data.card_created
    address_to_be_added = checkout_data.address_created
    delivery_selected = checkout_data.delivery_selected

    response_from_order_history = order_history.get_order_history(
        headers=headers_with_auth
    )

    validated_response = validate_response(GetOrderHistoryListSchema, response_from_order_history.json())

    assert_status_code(response_from_order_history, HTTPStatus.OK)

    assert_order_history_matches_order_data(
        response=validated_response,
        expected_product_data=selected_product,
        expected_payment_data=card_to_be_added,
        expected_address_data=address_to_be_added,
        expected_delivery_data=delivery_selected,
        tracking_order=checkout_response
    )
