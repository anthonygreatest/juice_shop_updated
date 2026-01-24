from data.locators.chatbot_locators import ChatbotLocators
from elements.image import Image
from elements.input import Input
from elements.text import Text
from pages.base_page import BasePage


class ChatbotPage(BasePage):

    WELCOMING_MESSAGE = lambda self, name: f'Nice to meet you {name}, I\'m Juicy'
    FIRST_MESSAGE = 'Help me'
    RANDOM_MESSAGE = 'Tell me about this shop'

    def __init__(self, page):
        super().__init__(page)
        self.locators = ChatbotLocators()
        self.message_from_bot = Text(page, self.locators.message_from_bot, 'Welcome message')
        self.profile_pic = Image(page, self.locators.profile_picture, 'Profile picture')
        self.message_input = Input(page, self.locators.message, 'Message')
        self.user_message_sent = Text(page, self.locators.user_message_sent, 'User Message')

    def check_chatbot_message_includes_username_set(self, expected_username):
        self.message_from_bot.check_contain_text(self.WELCOMING_MESSAGE(expected_username))

    def get_profile_pic(self):
        return self.profile_pic.get_attribute('src')

    def text_robot(self, message):
        self.message_input.scroll_into_view_if_needed()
        self.message_input.fill(message)
        self.message_input.check_have_value(message)
        self.message_input.press_enter()

    def read_bot_message(self, message):
        return self.message_from_bot.get_text(nth=message-1).strip()

    def check_sent_user_message_appears_in_chat(self, message):
        self.user_message_sent.check_contain_text(self.RANDOM_MESSAGE, nth=message-1)

