from data.locators.profile_page_locators import ProfilePageLocators
from elements.button import Button
from elements.file import File
from elements.image import Image
from elements.input import Input
from elements.text import Text
from pages.base_page import BasePage


class ProfilePage(BasePage):

    FILE_TOO_LARGE = 'MulterError: File too large'
    ILLEGAL_FILE_FORMAT = 'Error: Illegal file type'
    WRONG_FILE_FORMAT = 'Error: Profile image upload does not accept this file type: application/pdf'

    def __init__(self, page):
        super().__init__(page)
        self.locators = ProfilePageLocators()
        self.upload_profile_pic = File(page, self.locators.choose_picture_btn, 'Upload profile pic')
        self.upload_pic_btn = Button(page, self.locators.upload_picture_btn, 'Upload picture')
        self.username_input = Input(page, self.locators.username_field, 'Username')
        self.set_username_btn = Button(page, self.locators.set_username_btn, 'Set username')
        self.username = Text(page, self.locators.username_text, 'Username')
        self.uploaded_picture = Image(page, self.locators.picture_uploaded, 'Uploaded picture')
        self.picture_error = Text(page, self.locators.picture_error, 'Picture error')

    def set_username(self, username):
        self.username_input.fill(username)
        self.username_input.check_have_value(username)
        self.set_username_btn.check_enabled()
        self.set_username_btn.click()

    def check_set_username_appears_matches_expected(self, expected_username):
        self.username.check_contain_text(expected_username)

    def upload_picture(self, path):
        self.upload_profile_pic.upload(path)
        self.upload_pic_btn.check_enabled()
        self.upload_pic_btn.click()

    def get_picture(self):
        return self.uploaded_picture.get_attribute('src')

    def check_invalid_picture_error_appears_on_page(self, expected_error):
        self.picture_error.check_contain_text(expected_error)