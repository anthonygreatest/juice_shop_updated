
from http import HTTPStatus

import allure

from data.constants import CARD_DELETED_TEXT
from utils.assertions.address_assertions import assert_address_can_be_deleted
from utils.assertions.base_assertions import assert_status_code
from utils.assertions.credit_card_assertions import assert_num_of_cards_on_page_matches_expected
from utils.schemas.add_credit_card_resp_schema import AddCreditCardRespSchema, DeleteCreditCardsRespSchema
from utils.validators import validate_response


@allure.feature('Credit Card')
@allure.story('Valid saved payment options flow')
@allure.title('Credit card exists in my payment options')

class TestMyPaymentOptions:

    def test_credit_card_can_be_deleted(self, credit_card, create_credit_card, headers_with_auth):

        response = create_credit_card.response_raw

        validated_response = validate_response(AddCreditCardRespSchema, response.json())

        response_from_deleted = credit_card.delete_credit_card(
            card_id=validated_response.data.id,
            headers=headers_with_auth
        )

        card_deleted_validated_response = validate_response(DeleteCreditCardsRespSchema, response_from_deleted.json())

        assert_status_code(response_from_deleted, HTTPStatus.OK)

        assert_address_can_be_deleted(card_deleted_validated_response, CARD_DELETED_TEXT)

    def test_deleted_card_no_longer_appears_on_page(self, credit_card, create_credit_card, headers_with_auth):

        response = create_credit_card.response_raw

        validated_response = validate_response(AddCreditCardRespSchema, response.json())

        credit_card.delete_credit_card(
            card_id=validated_response.data.id,
            headers=headers_with_auth
        )

        all_cards = credit_card.get_credit_cards(
            headers=headers_with_auth
        )

        assert_num_of_cards_on_page_matches_expected(all_cards, num_of_cards=0)


