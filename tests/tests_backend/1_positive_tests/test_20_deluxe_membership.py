from http import HTTPStatus

import allure
import pytest

from data.constants import DELUXE_MEMBER_TEXT
from data.frontend_endpoints import PlaywrightEndpoints
from data.generators.order_generator import pick_product_to_purchase
from utils.assertions.base_assertions import assert_status_code

from utils.assertions.membership_assertions import assert_user_able_to_become_deluxe_member
from utils.helper import prepare_deluxe_membership_payload
from utils.schemas.deluxe_membership_resp_schema import DeluxeRespSchema
from utils.validators import validate_response


@pytest.mark.delete_card
@allure.feature('Deluxe Membership')
@allure.story('Valid deluxe membership flow')
class TestDeluxeMembership:

    @allure.title('Successful deluxe subscription')
    def test_deluxe_membership_can_be_activated(self, create_credit_card, deluxe_membership, headers_with_auth):

        card_to_be_added = create_credit_card(headers_with_auth).added_card

        membership_request = prepare_deluxe_membership_payload(
            payment_mode='card',
            card_id=card_to_be_added.data.id
        )

        response = deluxe_membership.become_deluxe_member(
            data=membership_request,
            headers=headers_with_auth
        )

        validated_response = validate_response(DeluxeRespSchema, response.json())

        assert_status_code(response, HTTPStatus.OK)
        assert_user_able_to_become_deluxe_member(validated_response, DELUXE_MEMBER_TEXT)
