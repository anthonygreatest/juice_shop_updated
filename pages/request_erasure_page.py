from data.locators.request_erasure_locators import RequestErasureLocators
from elements.button import Button
from elements.input import Input
from elements.link import Link
from elements.text import Text
from pages.all_products_page import AllProductsPage
from pages.base_page import BasePage

class RequestErasurePage(BasePage):

    GOODBYE_MESSAGE = 'Sorry to see you leave! Your erasure request will be processed shortly.'

    def __init__(self, page):
        super().__init__(page)
        self.locators = RequestErasureLocators()
        self.email_address_input = Input(page, self.locators.email_field, 'Email Address')
        self.security_question_input = Input(page, self.locators.security_question, 'Security Question')
        self.erase_data_btn = Button(page, self.locators.erase_data_btn, 'Erase Data')
        self.goodbye_text = Text(page, self.locators.goodbye_message, 'Goodbye Message')
        self.go_to_homepage_btn = Link(page, self.locators.go_to_homepage_btn, 'Go to homepage')

    def check_email_and_security_question_in_placeholder_match_expected(self, expected_email, expected_sec_question):
        self.email_address_input.check_have_attribute(attribute='placeholder', value=expected_email)
        self.security_question_input.check_have_attribute(attribute='placeholder', value=expected_sec_question.capitalize())

    def request_data_erasure(self, email, answer):
        self.email_address_input.fill(email)
        self.security_question_input.fill(answer)
        self.erase_data_btn.check_enabled()
        self.erase_data_btn.click()

    def check_goodbye_message_appears_on_page(self):
        self.goodbye_text.check_contain_text(self.GOODBYE_MESSAGE)

    def go_to_homepage(self):
        self.go_to_homepage_btn.hover()
        self.go_to_homepage_btn.click(force=True)

        return AllProductsPage(self.page)
