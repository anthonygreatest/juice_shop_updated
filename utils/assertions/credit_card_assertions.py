import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.add_credit_card_request import AddCreditCardRequest
from utils.schemas.add_credit_card_resp_schema import AddCreditCardRespSchema, GetCreditCardsRespSchema, \
    DeleteCreditCardsRespSchema


logger = get_logger("CARD_ASSERTIONS")

@allure.step('Checking credit card gets added')
def assert_added_card_gets_saved(response: AddCreditCardRespSchema, expected: AddCreditCardRequest):

    logger.info('Checking credit card gets added')

    assert_match(response.data.full_name, expected.full_name, 'full name')
    assert_match(response.data.card_num, expected.card_num, 'card num')
    assert_match(response.data.exp_year, int(expected.exp_year), 'exp year')
    assert_match(response.data.exp_month, int(expected.exp_month), 'exp month')

@allure.step('Checking credit card gets added')
def assert_added_card_appears_among_others(response: GetCreditCardsRespSchema, expected: AddCreditCardRequest):

    logger.info('Checking credit card gets added')

    matched_card = next(
        (card for card in response.data if card.full_name == expected.full_name),
        None
    )

    assert matched_card, f'Credit card with {expected.full_name} not found'

    assert_match(matched_card.full_name, expected.full_name, 'full name')
    assert_match(matched_card.card_num, '*'*12 + str(expected.card_num)[-4:], 'card num hidden')
    assert_match(matched_card.exp_year, int(expected.exp_year), 'exp year')
    assert_match(matched_card.exp_month, int(expected.exp_month), 'exp month')

@allure.step('Checking credit card gets deleted')
def assert_card_can_be_deleted(response: DeleteCreditCardsRespSchema, expected_text: str):

    assert_match(response.data, expected_text, 'data text')

@allure.step('Checking credit card gets deleted')
def assert_num_of_cards_on_page_matches_expected(response: GetCreditCardsRespSchema, num_of_cards: int):

    assert_match(len(response.data), num_of_cards, 'num of cards')

@allure.step('Checking credit card gets deleted')
def check_num_of_cards_on_page_matches_expected(actual_num: int, expected_num: int):

    assert_match(actual_num, expected_num, 'num of cards')