import allure
import pytest
from data.frontend_endpoints import PlaywrightEndpoints
from tests.tests_frontend.frontend_helpers import generate_feedback

@pytest.mark.usefixtures('close_cookies_banner')
@allure.feature('Customer Feedback')
@allure.story('Valid customer feedback flow')
class TestCustomerFeedback:

    @allure.title('Customer feedback toast appears on page')
    def test_customer_feedback_toast_appears_on_page(self, customer_feedback_page):

        feedback = generate_feedback()

        customer_feedback_page.open(PlaywrightEndpoints.CUSTOMER_FEEDBACK)
        customer_feedback_page.leave_feedback(
            comment=feedback.comment,
            rating=feedback.rating
        )

        customer_feedback_page.check_thanks_for_feedback_text_appears_on_page()

    @allure.title('Customer feedback gets saved on about us page')
    def test_customer_feedback_is_saved_on_about_us_page(self, about_us_page, customer_feedback_page,
        send_feedback, get_headers, register_response_via_ui):

        response, feedback_to_send = send_feedback(
            headers=get_headers,
            register_response=register_response_via_ui
        )

        about_us_page.open(PlaywrightEndpoints.ABOUT_US)
        about_us_page.check_comment_appears_among_others_on_page(
            comment=feedback_to_send.comment
        )


