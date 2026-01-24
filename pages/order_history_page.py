from decimal import Decimal
from components.basket_component import BasketComponent
from components.product_card_component import ProductCardComponent
from components.toast_component import ToastComponent
from data.dataclasses.selected_product_data import SelectedProductData
from data.locators.order_history_page_locators import OrderHistoryPageLocators
from elements.button import Button
from elements.link import Link
from elements.text import Text
from pages.base_page import BasePage
from utils.schemas.delivery_options_resp_schema import DeliveryOptionsRespSchema
from utils.schemas.write_reviews_request_schema import WriteReviewsRequestSchema


class OrderHistoryPage(BasePage):

    REVIEW_SAVED_TEXT = 'You review has been saved.'

    def __init__(self, page):
        super().__init__(page)
        self.locators = OrderHistoryPageLocators()
        self.basket = BasketComponent(page)
        self.print_order_confirm_btn = Button(page, self.locators.print_order_confirmation_btn, 'Print Order Confirmation Button')
        self.twitter_link = Link(page, self.locators.twitter, 'Post on Twitter Link')
        self.write_review_btn = Button(page, self.locators.write_review_btn, 'Write a review Button')
        self.order_info = Text(page, self.locators.order_info, 'Order Info')
        self.product_card = ProductCardComponent(page)
        self.toast = ToastComponent(page)
        self.comments = Text(page, self.locators.comments, 'Comment')

    def check_order_history_data_matches_expected(self, expected_selected_product_data: SelectedProductData,
        expected_tracking_num: str, expected_delivery_data: DeliveryOptionsRespSchema):

        self.basket.product_info.check_have_text(expected_selected_product_data.product_name, nth=0)
        self.basket.product_info.check_contain_text(str(expected_selected_product_data.product_price), nth=1)
        self.order_info.check_contain_text(expected_tracking_num, nth=0)

        product_price = Decimal(str(expected_selected_product_data.product_price))
        self.order_info.check_contain_text(
            str(product_price + expected_delivery_data.data.price), nth=3)

    def click_write_review(self):
        self.write_review_btn.check_enabled(nth=0)
        self.write_review_btn.click(nth=0)

    def write_review(self, review):
        self.click_write_review()
        self.product_card.write_review(review)
        self.product_card.click_submit()

    def check_review_toast_text_matches_expected(self):
        self.toast.check_toast_text(self.REVIEW_SAVED_TEXT)

    def check_review_left_appears_among_others(self, review_left: WriteReviewsRequestSchema):
        self.comments.check_contain_text(str(review_left.author))
        self.comments.check_contain_text(review_left.message)

    def check_num_of_likes_matches_expected(self, expected_likes_num: int):
        self.product_card.likes_counter.check_contain_text(str(expected_likes_num))

