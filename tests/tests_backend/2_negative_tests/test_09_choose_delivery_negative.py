import random
from http import HTTPStatus

import allure
import pytest

from data.constants import DELIVERY_OPTIONS
from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import prepare_missing_headers


@allure.feature('Delivery')
@allure.story('Invalid delivery flow')
class TestChooseDeliveryNegative:

    @allure.title('User not able to choose nonexistent delivery')
    @pytest.mark.parametrize('option, expected', [
        (0, HTTPStatus.BAD_REQUEST),
        ('abc', HTTPStatus.BAD_REQUEST),
        (1, HTTPStatus.OK),
        (4, HTTPStatus.BAD_REQUEST)
    ])
    def test_choose_delivery_with_nonexistent_id(self, delivery_options, headers_with_auth, option, expected):

        response = delivery_options.choose_delivery(
            option=option,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @allure.title('User not able to choose delivery with headers missing')
    def test_delivery_missing_headers(self, headers_with_auth, delivery_options):

        selected_option = random.choice(DELIVERY_OPTIONS)

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header='Authorization'
        )

        response = delivery_options.choose_delivery(
            option=selected_option,
            headers=bad_headers
        )

        assert_status_code(response, HTTPStatus.UNAUTHORIZED)

