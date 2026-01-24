from http import HTTPStatus

import allure
import pytest

from utils.assertions.base_assertions import assert_status_code
from utils.assertions.credit_card_assertions import assert_added_card_gets_saved, assert_added_card_appears_among_others
from utils.helper import add_credit_card_payload
from utils.schemas.add_credit_card_resp_schema import AddCreditCardRespSchema
from utils.validators import validate_response


@pytest.mark.delete_card
@allure.feature('Credit Card')
@allure.story('Valid credit card flow')
class TestCreateCreditCard:

    @allure.title('User able to add credit card')
    def test_user_able_to_add_credit_card(self, create_credit_card, headers_with_auth):

        card_data = create_credit_card(headers_with_auth)
        response = card_data.response_raw
        card_to_be_added = card_data.card_payload

        validated_response = validate_response(AddCreditCardRespSchema, response.json())

        assert_status_code(response, HTTPStatus.CREATED)

        assert_added_card_gets_saved(validated_response, card_to_be_added)

    @allure.title('Added credit card saved on cards page')
    def test_added_card_appears_on_cards_page(self, create_credit_card, credit_card, headers_with_auth):

        card_to_be_added = create_credit_card(headers_with_auth).card_payload

        all_cards = credit_card.get_credit_cards(
            headers=headers_with_auth
        )

        assert_added_card_appears_among_others(all_cards, card_to_be_added)

