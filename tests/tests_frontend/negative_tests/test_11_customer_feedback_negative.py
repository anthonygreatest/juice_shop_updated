import allure
import pytest

from data.frontend_endpoints import PlaywrightEndpoints
from data.generators.review_generator import FeedbackGenerator
from pages.customer_feedback_page import CustomerFeedbackPage
from tests.tests_frontend.frontend_helpers import generate_feedback


@pytest.mark.screenshot
@allure.feature('Customer Feedback')
@allure.story('Invalid customer feedback flow')
class TestCustomerFeedbackNegative:

    random_review = generate_feedback()

    @allure.title('User not able to send feedback with invalid data')
    @pytest.mark.parametrize('comment, rating, captcha, expected_error', [
        ('', 1, '', CustomerFeedbackPage.EMPTY_COMMENT),
        (random_review.comment, 1, '', CustomerFeedbackPage.EMPTY_CAPTCHA),
        (random_review.comment, 1, 'ABC', CustomerFeedbackPage.INVALID_CAPTCHA),
    ])
    def test_send_feedback_with_invalid_data(self, customer_feedback_page, comment, rating, captcha, expected_error):

        customer_feedback_page.open(PlaywrightEndpoints.CUSTOMER_FEEDBACK)
        customer_feedback_page.reload()
        customer_feedback_page.write_comment(
            comment
        )

        customer_feedback_page.give_rating(rating)

        customer_feedback_page.write_captcha_result(captcha)

        customer_feedback_page.check_invalid_field_error_appears_on_page(expected_error=expected_error)
        customer_feedback_page.check_submit_button_remains_disabled()

    @allure.title('User not able to request data export with wrong captcha')
    def test_send_feedback_without_rating(self, customer_feedback_page):
        feedback = generate_feedback()

        customer_feedback_page.open(PlaywrightEndpoints.CUSTOMER_FEEDBACK)
        customer_feedback_page.write_comment(
            feedback.comment
        )

        customer_feedback_page.write_captcha_result()

        customer_feedback_page.check_submit_button_remains_disabled()

    @allure.title('User not able to request data export with wrong captcha')
    def test_send_feedback_with_wrong_captcha_answer(self, customer_feedback_page):

        feedback = generate_feedback()
        captcha_answer = '0'

        customer_feedback_page.open(PlaywrightEndpoints.CUSTOMER_FEEDBACK)
        customer_feedback_page.write_comment(
            feedback.comment
        )

        customer_feedback_page.give_rating(feedback.rating)

        customer_feedback_page.captcha_input.fill(captcha_answer)
        customer_feedback_page.click_submit_comment()

        customer_feedback_page.check_wrong_captcha_toast_appears_on_page()
