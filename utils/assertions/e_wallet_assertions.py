from decimal import Decimal

import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.digital_wallet_request_schema import DigitalWalletRequestSchema
from utils.schemas.digital_wallet_resp_schema import DigitalWalletRespSchema
from utils.schemas.get_order_history_schema import GetOrderHistoryListSchema

logger = get_logger("E_WALLET_ASSERTIONS")

@allure.step('Checking money gets deposited')
def assert_money_gets_deposited_to_e_wallet(response: DigitalWalletRespSchema,
    expected: DigitalWalletRequestSchema):

    logger.info('Checking money gets deposited')

    assert_match(response.data, expected.balance, 'deposited sum')

@allure.step('Checking balance changed after purchase')
def assert_balance_changes_after_purchase(balance_before: DigitalWalletRespSchema,
    expected_balance: DigitalWalletRespSchema, deposit: GetOrderHistoryListSchema):

    logger.info('Checking balance changed after purchase')

    sum_paid = deposit.data[0].total_price

    assert balance_before.data - sum_paid == expected_balance.data

@allure.step('Checking money gets deposited')
def assert_balance_changes_after_deposit(response: DigitalWalletRespSchema,
    deposit: DigitalWalletRequestSchema, balance_before: DigitalWalletRespSchema):

    logger.info('Checking money gets deposited')

    assert_match(response.data, deposit.balance + balance_before.data, 'deposited sum')

@allure.step('Checking balance changes after paying membership fee')
def assert_balance_changes_after_paying_membership_fee(expected_balance: DigitalWalletRespSchema,
    current_balance: Decimal, fee: Decimal):

    logger.info('Checking balance changes after paying membership fee')

    assert_match(expected_balance.data, current_balance - fee, 'balance after paying membership fee')