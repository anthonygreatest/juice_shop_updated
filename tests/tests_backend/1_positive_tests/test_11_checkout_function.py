import random
from http import HTTPStatus

import allure
import pytest


from tests.conftest import checkout_factory
from utils.assertions.base_assertions import assert_status_code
from utils.schemas.checkout_resp_schema import CheckoutRespSchema
from utils.validators import validate_response


@pytest.mark.delete_address
@pytest.mark.delete_card
@allure.feature('Checkout')
@allure.story('Valid checkout flow')
@allure.title('User able to make an order at checkout')
def test_user_able_to_make_order_at_checkout(checkout_factory, headers_with_auth, login_response):

    response = checkout_factory(
        e_wallet=False,
        headers=headers_with_auth,
        login_response=login_response).checkout_response

    validate_response(CheckoutRespSchema, response.json())
    assert_status_code(response, HTTPStatus.OK)


