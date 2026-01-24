import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.deluxe_membership_resp_schema import DeluxeRespSchema


logger = get_logger("MEMBERSHIP_ASSERTIONS")

@allure.step('Checking user able to become deluxe member')
def assert_user_able_to_become_deluxe_member(response: DeluxeRespSchema, membership_text: str):

    logger.info('Checking user able to become deluxe member')

    assert_match(response.data.confirmation, membership_text, 'membership text')