import json
from http import HTTPStatus
import allure
import pytest
from data.endpoints import Endpoints
from utils.assertions.base_assertions import assert_status_code, assert_status_code_among_expected
from utils.helper import prepare_raw_deluxe_membership_payload, prepare_fresh_user, prepare_missing_headers, \
    deposit_money_to_e_wallet


@allure.feature('Deluxe Membership')
@allure.story('Invalid deluxe membership flow')
@pytest.mark.delete_card
class TestDeluxeMembershipNegative:

    @allure.title('User not able to become deluxe member with invalid data')
    @pytest.mark.parametrize('value, field, expected', [
        ('paymentId', 0, HTTPStatus.BAD_REQUEST),
        ('paymentId', 'a', HTTPStatus.BAD_REQUEST),
        ('paymentId', True, HTTPStatus.BAD_REQUEST),
        ('paymentId', None, HTTPStatus.BAD_REQUEST),
        ('paymentMode', 'card', HTTPStatus.OK),
        ('paymentMode', 'wallet', HTTPStatus.BAD_REQUEST),
        ('paymentMode', 1, HTTPStatus.BAD_REQUEST),
        ('paymentMode', 'paper', HTTPStatus.BAD_REQUEST),
        ('paymentMode', True, HTTPStatus.BAD_REQUEST),
        ('paymentMode', None, HTTPStatus.BAD_REQUEST),
    ])
    def test_deluxe_membership_invalid_data(self, raw_api_client, register, login, digital_wallet,
        create_credit_card, value, field, expected):

        new_user_headers = prepare_fresh_user(
            register=register,
            login=login
        )

        card_id = create_credit_card.added_card.data.id

        data = prepare_raw_deluxe_membership_payload(
            payment_mode='card',
            card_id=card_id
        )

        data[field] = value

        response = raw_api_client.post(
            endpoint='deluxe_membership',
            data=data,
            headers=new_user_headers
        )

        assert_status_code(response, expected)

    @allure.title('User not able to become deluxe member with missing fields')
    @pytest.mark.parametrize('missing_field, expected', [
        ('paymentId', HTTPStatus.BAD_REQUEST),
        ('paymentMode', HTTPStatus.BAD_REQUEST)
    ])
    def test_deluxe_membership_missing_fields(self, raw_api_client, create_credit_card,
        missing_field, expected, register, login):

        new_user_headers = prepare_fresh_user(
            register=register,
            login=login
        )

        card_id = create_credit_card.added_card.data.id

        data = prepare_raw_deluxe_membership_payload(
            payment_mode='card',
            card_id=card_id
        )

        data.pop(missing_field)

        response = raw_api_client.post(
            endpoint='deluxe_membership',
            data=data,
            headers=new_user_headers
        )

        assert_status_code(response, expected)

    @allure.title('User not able to become deluxe member with missing headers')
    @pytest.mark.parametrize('missing_header, codes', [
        ('Content-Type', [415, 400, 500, 401]),
        ('Authorization', [401])
    ])
    def test_deluxe_membership_missing_headers(self, raw_api_client, register, login,
        create_credit_card, missing_header, codes):

        new_user_headers = prepare_fresh_user(
            register=register,
            login=login
        )

        card_id = create_credit_card.added_card.data.id

        data = prepare_raw_deluxe_membership_payload(
            payment_mode='card',
            card_id=card_id
        )

        bad_headers = prepare_missing_headers(
            headers_with_auth=new_user_headers,
            missing_header=missing_header
        )

        response = raw_api_client.post_with_raw_headers(
            endpoint='deluxe_membership',
            data=data,
            headers=bad_headers
        )

        assert_status_code_among_expected(response, codes)

    @allure.title('User not able to become deluxe member with wrong HTTP method')
    def test_deluxe_membership_wrong_method(self, raw_api_client, register, login, create_credit_card):

        new_user_headers = prepare_fresh_user(
            register=register,
            login=login
        )

        card_id = create_credit_card.added_card.data.id

        params = prepare_raw_deluxe_membership_payload(
            payment_mode='card',
            card_id=card_id
        )

        response = raw_api_client.get(
            endpoint='deluxe_membership',
            params=params,
            headers=new_user_headers
        )

        assert_status_code(response, HTTPStatus.METHOD_NOT_ALLOWED)