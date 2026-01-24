from playwright.sync_api import Page

from components.base_component import BaseComponent
from data.locators.order_history_page_locators import OrderHistoryPageLocators
from elements.button import Button
from elements.input import Input
from elements.text import Text


class ProductCardComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = OrderHistoryPageLocators
        self.open_reviews_btn = Button(page, self.locators.expand_review_btn, 'Open reviews')
        self.like_btn = Button(page, self.locators.like_a_review_btn, 'Like a review')
        self.likes_cnt = Text(page, self.locators.like_counter, 'Num of likes under review')
        self.review_input = Input(page, self.locators.review_field, 'Review')
        self.submit_btn = Button(page, self.locators.submit_review_btn, 'Submit review')
        self.likes_counter = Text(page, self.locators.like_counter, 'Likes counter')

    def click_open_reviews(self):
        self.open_reviews_btn.check_enabled()
        self.open_reviews_btn.click()

    def leave_a_like(self):
        self.like_btn.check_enabled(nth=0)
        self.like_btn.click(nth=0)

    def write_review(self, review):
        self.review_input.wait_for_selector(self.locators.write_review_container)
        self.review_input.scroll_into_view_if_needed()
        self.review_input.fill(review)
        self.review_input.check_have_value(review)

    def click_submit(self):
        self.submit_btn.check_enabled()
        self.submit_btn.click()

    def count_likes(self):
        likes = self.likes_counter.get_text(nth=0)
        return int(likes)
