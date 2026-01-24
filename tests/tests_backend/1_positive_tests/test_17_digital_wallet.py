from http import HTTPStatus

import allure
import pytest

from utils.assertions.base_assertions import assert_status_code
from utils.assertions.e_wallet_assertions import assert_money_gets_deposited_to_e_wallet, \
    assert_balance_changes_after_deposit
from utils.helper import deposit_money_to_e_wallet
from utils.schemas.digital_wallet_resp_schema import DigitalWalletRespSchema
from utils.validators import validate_response


@pytest.mark.delete_card
@allure.feature('Digital wallet')
@allure.story('Valid digital wallet flow')
class TestDigitalWallet:

    @allure.title('Deposited sum appears in digital wallet')
    def test_deposited_sum_appears_in_digital_wallet(self, digital_wallet, headers_with_auth, create_credit_card):
        card_to_be_added = create_credit_card(headers_with_auth).added_card

        deposit_data = deposit_money_to_e_wallet(
            payment_id=card_to_be_added.data.id,
            headers=headers_with_auth,
            digital_wallet=digital_wallet,
            balance='random'
        )

        digital_wallet_balance = digital_wallet.get_digital_wallet_balance(
            headers=headers_with_auth
        )

        assert_balance_changes_after_deposit(
            response=digital_wallet_balance,
            deposit=deposit_data.deposit_payload,
            balance_before=deposit_data.balance_before_deposit
        )


    @allure.title('User able to deposit money to digital wallet')
    def test_money_can_be_deposited_to_digital_wallet(self, digital_wallet, headers_with_auth, create_credit_card):
        card_to_be_added = create_credit_card(headers_with_auth).added_card

        deposit_data = deposit_money_to_e_wallet(
            payment_id=card_to_be_added.data.id,
            headers=headers_with_auth,
            digital_wallet=digital_wallet,
            balance='random'
        )

        validated_response = validate_response(DigitalWalletRespSchema, deposit_data.response_raw.json())

        assert_status_code(deposit_data.response_raw, HTTPStatus.OK)
        assert_money_gets_deposited_to_e_wallet(validated_response, deposit_data.deposit_payload)


