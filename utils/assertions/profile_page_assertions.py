import allure

from utils.logger import get_logger

logger = get_logger("PROFILE_PAGE_ASSERTIONS")

@allure.step('Checking profile picture gets updated')
def assert_profile_picture_gets_updated(old_picture: str, updated_picture: str):

    logger.info('Checking profile picture gets updated')

    assert updated_picture != old_picture