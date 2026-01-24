import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger

logger = get_logger("ADDRESS_ASSERTIONS")

@allure.step('Checking outer source link present on about us page')
def assert_outer_source_link_present_on_about_us_page(actual_link, expected_link):

    logger.info('Checking outer source link present on about us page')

    assert_match(actual_link, expected_link, 'outer source link')