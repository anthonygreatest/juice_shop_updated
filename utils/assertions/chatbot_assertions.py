import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.robot_resp_schema import RobotRespSchema, RobotRequestSchema

logger = get_logger("CHATBOT_ASSERTIONS")

@allure.step('Checking chatbot query gets sent')
def assert_chatbot_query_gets_sent(response: RobotRespSchema, expected_name: str):

    logger.info('Checking chatbot query gets sent')

    assert expected_name in response.body

@allure.step('Checking photo in chatbot chat matches expected')
def assert_photo_in_chat_matches_expected(photo_in_chat: str, expected_photo: str):

    logger.info('Checking photo in chatbot chat matches expected')

    assert_match(photo_in_chat, expected_photo, 'photo in chat')

@allure.step('Checking chatbot replies to user messages')
def check_chatbot_replies_to_user_messages(reply_from_bot):

    logger.info('Checking chatbot replies to user messages')

    assert len(reply_from_bot) != 0
