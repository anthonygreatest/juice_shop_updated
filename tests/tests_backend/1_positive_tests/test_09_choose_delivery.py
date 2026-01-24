import random
from http import HTTPStatus

import allure

from data.constants import DELIVERY_OPTIONS
from utils.assertions.base_assertions import assert_status_code
from utils.assertions.delivery_assertions import assert_delivery_option_selected
from utils.schemas.delivery_options_resp_schema import DeliveryOptionsRespSchema
from utils.validators import validate_response


@allure.feature('Delivery')
@allure.story('Valid delivery flow')
class TestDeliveryOptions:

    @allure.title('User able to select delivery option')
    def test_delivery_option_gets_selected(self, delivery_options, headers_with_auth):

        selected_option = random.choice(DELIVERY_OPTIONS)

        response = delivery_options.choose_delivery(
            option=selected_option,
            headers=headers_with_auth
        )

        validated_response = validate_response(DeliveryOptionsRespSchema, response.json())

        assert_status_code(response, HTTPStatus.OK)

        assert_delivery_option_selected(validated_response, selected_option)
