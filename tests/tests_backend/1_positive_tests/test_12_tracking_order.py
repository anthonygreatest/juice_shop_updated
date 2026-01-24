from http import HTTPStatus

import allure
import pytest
from utils.assertions.base_assertions import assert_status_code
from utils.assertions.tracking_order_assertions import assert_tracking_order_data_matches_order_data
from utils.helper import prepare_checkout_response
from utils.schemas.get_order_history_schema import GetOrderHistoryListSchema
from utils.validators import validate_response


@pytest.mark.delete_address
@pytest.mark.delete_card
@allure.feature('Tracking Order')
@allure.story('Valid tracking order flow')
@allure.title('Order confirmation data matches actual order data')
def test_order_confirmation_data_matches_order_data(checkout_factory, tracking_order, headers_with_auth, login_response):

    checkout_data = checkout_factory(e_wallet=False, headers=headers_with_auth, login_response=login_response)
    checkout_response = prepare_checkout_response(checkout_data)

    selected_product = checkout_data.selected_product
    card_to_be_added = checkout_data.card_created
    address_to_be_added = checkout_data.address_created
    delivery_selected = checkout_data.delivery_selected

    response_from_tracking_order = tracking_order.get_tracking_order(
        tracking_id=checkout_response.order_confirmation,
        headers=headers_with_auth
    )

    validated_response = validate_response(GetOrderHistoryListSchema, response_from_tracking_order.json())

    assert_status_code(response_from_tracking_order, HTTPStatus.OK)

    assert_tracking_order_data_matches_order_data(
        response=validated_response,
        expected_product_data=selected_product,
        expected_payment_data=card_to_be_added,
        expected_address_data=address_to_be_added,
        expected_delivery_data=delivery_selected,
        tracking_order=checkout_response
    )







