import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from utils.helper import prepare_checkout_response


@allure.feature('Order History')
@allure.story('Valid order history flow')
@pytest.mark.usefixtures('close_cookies_banner')
@pytest.mark.delete_address
@pytest.mark.delete_card
class TestOrderHistory:

    @allure.title('Order appears on history page')
    def test_order_appears_on_order_history_page(self, order_history_page, checkout_factory, get_headers, basket_id):

        checkout_data = checkout_factory(e_wallet=False, headers=get_headers, login_response=basket_id)
        order_confirmation = prepare_checkout_response(checkout_data).order_confirmation

        order_history_page.open(PlaywrightEndpoints.ORDER_HISTORY)

        order_history_page.check_order_history_data_matches_expected(
            expected_selected_product_data=checkout_data.product_name_and_price,
            expected_tracking_num=order_confirmation,
            expected_delivery_data=checkout_data.delivery_selected
        )

    @allure.title('Review saved success toast appears on page')
    def test_leave_review_toast_appears_on_order_history_page(self, write_review, order_history_page):

        write_review(
            review_page=order_history_page,
            url=PlaywrightEndpoints.ORDER_HISTORY
        )

        order_history_page.check_review_toast_text_matches_expected()

    @allure.title('Review appears among other reviews')
    def test_review_left_appears_among_other_reviews(self, write_review, order_history_page):

        review_left = write_review(
            review_page=order_history_page,
            url=PlaywrightEndpoints.ORDER_HISTORY
        )

        order_history_page.product_card.click_open_reviews()

        order_history_page.check_review_left_appears_among_others(
            review_left=review_left
        )

    @allure.title('Like appears on page')
    def test_leave_a_like_from_order_history_page(self, write_review, order_history_page):

        write_review(
            review_page=order_history_page,
            url=PlaywrightEndpoints.ORDER_HISTORY
        )

        order_history_page.product_card.click_open_reviews()

        likes_before = order_history_page.product_card.count_likes()

        order_history_page.product_card.leave_a_like()

        order_history_page.check_num_of_likes_matches_expected(
            expected_likes_num=likes_before + 1
        )







