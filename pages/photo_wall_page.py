from components.toast_component import ToastComponent
from data.locators.photo_wall_locators import PhotoWallLocators
from elements.button import Button
from elements.file import File
from elements.image import Image
from elements.input import Input
from elements.text import Text
from pages.base_page import BasePage
from pages.mixins import FileUploader, NegativeTestsMixin


class PhotoWallPage(BasePage, FileUploader, NegativeTestsMixin):

    IMAGE_UPLOADED_TOAST = 'Your image was successfully uploaded.'
    EMPTY_CAPTION = 'Please enter a caption'

    def __init__(self, page):
        super().__init__(page)
        self.locators = PhotoWallLocators()
        self.caption_input = Input(page, self.locators.caption, 'Caption')
        self.pick_image = File(page, self.locators.pick_image, 'Upload photo')
        self.submit_btn = Button(page, self.locators.submit_btn, 'Submit')
        self.toast = ToastComponent(page)
        self.post = Image(page, self.locators.post, 'Post')
        self.field_error = Text(page, self.ERROR, 'Field error')

    def click_submit(self):
        self.submit_btn.check_enabled()
        self.submit_btn.click()

    def write_caption(self, caption):
        self.caption_input.scroll_into_view_if_needed()
        self.caption_input.fill(caption)
        self.caption_input.check_have_value(caption)
        self.caption_input.blur()

    def attach_photo(self, caption, path):
        self.write_caption(caption)
        self.pick_image.upload(path)
        self.click_submit()

    def check_img_uploaded_toast_appears_on_page(self):
        self.toast.check_toast_text(self.IMAGE_UPLOADED_TOAST)

    def check_post_appears_on_page(self, expected_comment):
        self.post.check_contain_text(expected_comment, nth=-1)

    def check_send_button_remains_disabled(self):
        self.submit_btn.check_disabled()

    def check_invalid_field_error_appears_on_page(self):
        self.field_error.check_have_text(self.EMPTY_CAPTION)



