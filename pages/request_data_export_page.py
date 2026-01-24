import json

from data.locators.request_data_export_locators import RequestDataExportLocators
from elements.button import Button
from elements.input import Input
from elements.text import Text
from pages.base_page import BasePage
from pages.mixins import NegativeTestsMixin
from utils.schemas.data_export_resp_schema import DataExportRespSchemaInside


class RequestDataExportPage(BasePage, NegativeTestsMixin):

    WRONG_CAPTCHA = 'Wrong answer to CAPTCHA. Please try again.'
    EMPTY_CAPTCHA = 'Please enter the result of the CAPTCHA.'

    def __init__(self, page):
        super().__init__(page)
        self.locators = RequestDataExportLocators()
        self.format_btn = Button(page, self.locators.json_export_btn, 'Select JSON format Button')
        self.request_btn = Button(page, self.locators.request_btn, 'Request Button')
        self.captcha_input = Input(page, self.locators.captcha_input_field, 'Captcha')
        self.form_error = Text(page, self.locators.form_error, 'Form error')

    def select_export_format(self):
        self.format_btn.check_enabled()
        self.format_btn.click()

    def click_request(self):
        self.request_btn.check_enabled()
        self.request_btn.click()

    def request_data_export_without_captcha(self):
        self.select_export_format()
        with self.page.context.expect_page() as new_page_info:
            self.click_request()
        new_window = new_page_info.value
        data = DataExportRespSchemaInside(**json.loads(new_window.locator('body').inner_text()))
        self.page.bring_to_front()
        new_window.close()
        return data

    def select_export_format_and_fill_in_captcha(self, captcha_answer):
        self.select_export_format()
        self.captcha_input.fill(captcha_answer)

    def request_data_export(self, captcha_answer):
        self.select_export_format_and_fill_in_captcha(captcha_answer)
        with self.page.context.expect_page() as new_page_info:
            self.click_request()
        new_window = new_page_info.value
        data = DataExportRespSchemaInside(**json.loads(new_window.locator('body').inner_text()))
        self.page.bring_to_front()
        new_window.close()
        return data

    def check_invalid_captcha_error_appears_on_page(self):
        self.form_error.check_have_text(self.WRONG_CAPTCHA)

    def check_request_button_remains_disabled(self):
        self.request_btn.check_disabled()
