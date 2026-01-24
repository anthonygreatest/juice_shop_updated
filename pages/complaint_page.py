from data.locators.complaint_page_locators import ComplaintPageLocators
from elements.button import Button
from elements.file import File
from elements.input import Input
from elements.text import Text
from pages.base_page import BasePage
from pages.mixins import FileUploader, NegativeTestsMixin


class ComplaintPage(BasePage, FileUploader, NegativeTestsMixin):

    CUSTOMER_SUPPORT_RESPONSE = 'Customer support will get in touch with you soon! Your complaint reference is #'
    WRONG_ATTACHED_FILE_TYPE = 'Forbidden file type. Only PDF, ZIP allowed.'
    EMPTY_COMPLAINT = 'Please provide a text.'

    def __init__(self, page):
        super().__init__(page)
        self.locators = ComplaintPageLocators()
        self.complaint_input = Input(page, self.locators.message, 'Complaint message')
        self.submit_btn = Button(page, self.locators.submit_btn, 'Submit')
        self.upload_complaint = File(page, self.locators.choose_file, 'Upload complaint')
        self.confirmation_text = Text(page, self.locators.confirmation, 'Confirmation')
        self.form_error = Text(page, self.locators.form_error, 'Form error')
        self.field_error = Text(page, self.ERROR, 'Field error')

    def write_message(self, message):
        self.complaint_input.fill(message)
        self.complaint_input.check_have_value(message)
        self.complaint_input.blur()

    def attach_complaint(self, path):
        self.upload_complaint.upload(path)
        self.submit_btn.check_enabled()
        self.submit_btn.click()

    def check_complaint_filed_confirmation_text_appears_on_page(self):
        self.confirmation_text.check_contain_text(self.CUSTOMER_SUPPORT_RESPONSE)

    def check_wrong_file_format_error_appears_on_page(self):
        self.form_error.check_have_text(self.WRONG_ATTACHED_FILE_TYPE)

    def check_submit_button_remains_disabled(self):
        self.submit_btn.check_disabled()

    def check_invalid_field_error_appears_on_page(self):
        self.field_error.check_have_text(self.EMPTY_COMPLAINT)
