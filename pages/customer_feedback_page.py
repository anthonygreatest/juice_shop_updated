import re

from components.toast_component import ToastComponent
from data.locators.customer_feedback_locators import CustomerFeedbackLocators
from elements.button import Button
from elements.input import Input
from elements.slider import Slider
from elements.text import Text
from pages.base_page import BasePage
from pages.mixins import NegativeTestsMixin


class CustomerFeedbackPage(BasePage, NegativeTestsMixin):

    THANKS_FOR_FEEDBACK_TEXT = 'Thank you for your feedback.'
    THANKS_FOR_GREAT_FEEDBACK_TEXT = 'Thank you so much for your amazing 5-star feedback!'
    EMPTY_CAPTCHA = 'Please enter the result of the CAPTCHA.'
    EMPTY_COMMENT = 'Please provide a comment.'
    INVALID_CAPTCHA = 'Invalid CAPTCHA code'
    WRONG_CAPTCHA = 'Wrong answer to CAPTCHA. Please try again.'

    def __init__(self, page):
        super().__init__(page)
        self.locators = CustomerFeedbackLocators()
        self.feedback_input = Input(page, self.locators.comment, 'Feedback')
        self.captcha_input = Input(page, self.locators.captcha_result, 'Captcha')
        self.submit_btn = Button(page, self.locators.submit_btn, 'Submit')
        self.rating_slider = Slider(page, self.locators.rating_slider, 'Rating slider')
        self.captcha_text = Text(page, self.locators.captcha, 'Captcha')
        self.toast = ToastComponent(page)
        self.field_error = Text(page, self.ERROR, 'Field error')

    def write_comment(self, comment):
        self.feedback_input.fill(comment)
        self.feedback_input.check_have_value(comment)
        self.feedback_input.blur()

    def solve_captcha(self):
        res = self.captcha_text.get_text()
        return eval(res)

    def give_rating(self, stars):
        # slider = self.get_locator(self.locators.rating_slider)
        self.rating_slider.focus()
        for _ in range(stars - 1):
            if stars == 1:
                self.rating_slider.press_right()
                self.rating_slider.press_left()
            self.rating_slider.press_right()

    def leave_feedback(self, comment, rating):
        self.write_comment(comment)
        self.give_rating(rating)
        result = self.solve_captcha()
        self.write_captcha_result(result)
        self.click_submit_comment()

    def write_captcha_result(self, result):
        self.captcha_input.fill(str(result))
        self.captcha_input.check_have_value(str(result))
        self.captcha_input.blur()

    def click_submit_comment(self):
        self.submit_btn.check_enabled()
        self.submit_btn.click()

    def check_thanks_for_feedback_text_appears_on_page(self):
        self.toast.check_toast_text(re.compile(f'{self.THANKS_FOR_FEEDBACK_TEXT}|{self.THANKS_FOR_GREAT_FEEDBACK_TEXT}'))

    def check_submit_button_remains_disabled(self):
        self.submit_btn.check_disabled()

    def check_wrong_captcha_toast_appears_on_page(self):
        self.toast.check_toast_text(self.WRONG_CAPTCHA)

    def check_invalid_field_error_appears_on_page(self, expected_error):
        self.field_error.check_contain_text(expected_error)