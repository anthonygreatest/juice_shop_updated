import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from utils.assertions.chatbot_assertions import assert_photo_in_chat_matches_expected, \
    check_chatbot_replies_to_user_messages


@pytest.mark.usefixtures('close_cookies_banner')
@allure.feature('Chatbot')
@allure.story('Valid chatbot flow')
class TestChatbot:

    @allure.title('Updated name appears on chatbot page')
    def test_changed_name_appears_on_chatbot_page(self, chatbot_page, updated_profile):

        pic_src_after_update, name = updated_profile

        chatbot_page.open(PlaywrightEndpoints.CHATBOT)

        chatbot_page.check_chatbot_message_includes_username_set(
            expected_username=name
        )

    @allure.title('Updated photo appears on chatbot page')
    def test_changed_photo_appears_on_chatbot_page(self, chatbot_page, updated_profile):

        pic_src_after_update, name = updated_profile

        chatbot_page.open(PlaywrightEndpoints.CHATBOT)
        chatbot_page.text_robot(chatbot_page.FIRST_MESSAGE)

        pic_src_on_chatbot_page = chatbot_page.get_profile_pic()

        assert_photo_in_chat_matches_expected(
            photo_in_chat=pic_src_on_chatbot_page,
            expected_photo=pic_src_after_update
        )

    @allure.title('User messages appear in chat')
    def test_user_messages_appear_in_chat(self, chatbot_page, updated_profile):

        chatbot_page.open(PlaywrightEndpoints.CHATBOT)
        chatbot_page.text_robot(chatbot_page.RANDOM_MESSAGE)

        chatbot_page.check_sent_user_message_appears_in_chat(
            message=1
        )

    @allure.title('Chatbot replies to user messages')
    def test_chatbot_replies_to_messages(self, chatbot_page, updated_profile):

        chatbot_page.open(PlaywrightEndpoints.CHATBOT)
        chatbot_page.text_robot(chatbot_page.RANDOM_MESSAGE)

        reply_from_bot = chatbot_page.read_bot_message(message=2)

        check_chatbot_replies_to_user_messages(
            reply_from_bot=reply_from_bot
        )

