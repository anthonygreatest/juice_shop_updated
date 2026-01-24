from http import HTTPStatus
import allure

from utils.assertions.base_assertions import assert_status_code
from utils.assertions.feedback_assertions import assert_customer_feedback_appears_among_comments, assert_customer_feedback_gets_sent
from utils.schemas.send_feedback_resp_schema import FeedbackRespSchema
from utils.validators import validate_response


@allure.feature('Feedback')
@allure.story('Valid feedback flow')
class TestCustomerFeedback:

    @allure.title('Customer feedback gets sent successfully')
    def test_user_able_to_send_feedback(self, send_feedback, headers_with_auth, register_response):

        response, feedback_to_send = send_feedback(
            headers=headers_with_auth,
            register_response=register_response
        )

        validated_response = validate_response(FeedbackRespSchema, response.json())

        assert_status_code(response, HTTPStatus.CREATED)

        assert_customer_feedback_gets_sent(validated_response, feedback_to_send)


    @allure.title('Sent feedback appears on feedback page')
    def test_sent_feedback_appears_on_feedback_page(self, headers_with_auth, send_feedback, customer_feedback,
        register_response):

        response, feedback_to_send = send_feedback(
            headers=headers_with_auth,
            register_response=register_response
        )

        all_comments = customer_feedback.get_feedback(
            headers=headers_with_auth
        )

        assert_customer_feedback_appears_among_comments(all_comments, feedback_to_send)