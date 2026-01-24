from http import HTTPStatus

import allure
import pytest

from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import prepare_missing_headers, prepare_checkout_response


@allure.feature('Tracking Order')
@allure.story('Invalid tracking order flow')
class TestTrackingOrderNegative:

    @allure.title('User not able to track order with invalid data')
    @pytest.mark.delete_address
    @pytest.mark.delete_card
    @pytest.mark.parametrize('tracking_num, expected', [
        (0, HTTPStatus.BAD_REQUEST),
        ('abc', HTTPStatus.BAD_REQUEST)
    ])
    def test_tracking_order_invalid_data(self, headers_with_auth, tracking_order, tracking_num, expected):

        response = tracking_order.get_tracking_order(
            tracking_id=tracking_num,
            headers=headers_with_auth
        )

        assert_status_code(response, expected)

    @pytest.mark.skip
    @allure.title('User not able to track order with missing headers')
    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [400, 415, 500, 200]),
        ('Authorization', [401])
    ])
    def test_tracking_order_missing_headers(self, checkout_factory, headers_with_auth, tracking_order, missing_header, codes):

        checkout_data = checkout_factory(e_wallet=False)
        checkout_response = prepare_checkout_response(checkout_data)

        bad_headers = prepare_missing_headers(
            headers_with_auth=headers_with_auth,
            missing_header=missing_header
        )

        response = tracking_order.get_tracking_order(
            tracking_id=checkout_response.order_confirmation,
            headers=bad_headers
        )

        assert_status_code_among_expected(response, codes)