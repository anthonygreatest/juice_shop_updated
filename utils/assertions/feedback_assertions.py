import allure

from utils.assertions.base_assertions import assert_match
from utils.clients.event_hooks import get_logger
from utils.schemas.send_feedback_request_schema import SendFeedbackRequestSchema
from utils.schemas.send_feedback_resp_schema import FeedbackRespSchema

logger = get_logger("FEEDBACK_ASSERTIONS")

@allure.step('Checking customer feedback gets sent')
def assert_customer_feedback_gets_sent(response: FeedbackRespSchema, expected: SendFeedbackRequestSchema):

    logger.info('Checking customer feedback gets sent')

    assert_match(response.data.user_id, expected.user_id, 'user id')
    assert_match(response.data.comment, expected.comment, 'comment')
    assert_match(response.data.rating, expected.rating, 'rating')

@allure.step('Checking customer feedback on feedback page')
def assert_customer_feedback_appears_among_comments(response: FeedbackRespSchema, expected: SendFeedbackRequestSchema):

    logger.info('Checking customer feedback on feedback page')

    assert any(expected.comment == feedback.comment for feedback in response.data)