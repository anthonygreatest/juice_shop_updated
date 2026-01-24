from playwright.sync_api import Page

from components.base_component import BaseComponent
from data.locators.about_us_page_locators import AboutUsPageLocators
from elements.button import Button
from elements.slider import Slider
from elements.text import Text


class GalleryComponent(BaseComponent):


    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = AboutUsPageLocators()
        # self.item = Text(page, self.locators.item, 'Feedback')
        self.next_item_btn = Button(page, self.locators.next_item_btn, 'Next item')
        self.gallery = Slider(page, self.locators.gallery, 'Gallery')
        self.comment_under_pic = Text(page, self.locators.comment_under_pic, 'Last comment')

    def navigate_to_last_post(self):
        cnt = self.page.locator(self.locators.item).count()
        self.gallery.scroll_into_view_if_needed()
        for _ in range(cnt - 1):
            self.next_item_btn.click()
        self.page.wait_for_selector(self.locators.gallery_item)
