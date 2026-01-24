import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger

logger = get_logger("SEARCH_PAGE_ASSERTIONS")

@allure.step('Checking num of items per page matches expected')
def assert_num_of_items_on_page_matches_expected(actual_items_num: int, expected_items_num: int):

    logger.info('Checking num of items per page matches expected')

    assert_match(actual_items_num, expected_items_num, 'num of items per page')