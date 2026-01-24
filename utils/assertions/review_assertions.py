import allure

from utils.assertions.base_assertions import assert_match
from utils.logger import get_logger
from utils.schemas.get_reviews_resp_schema import GetReviewsRespSchema
from utils.schemas.like_review_resp_schema import LikeReviewRespSchema

logger = get_logger("REVIEW_ASSERTIONS")

@allure.step('Checking like gets added')
def assert_like_gets_added(response: LikeReviewRespSchema, expected_email: str):

    logger.info('Checking like gets added')

    assert any(expected_email in resp.liked_by for resp in response.updated)


@allure.step('Checking like appears under review')
def assert_like_appears_under_review(response: LikeReviewRespSchema, expected_cnt: int):

    logger.info('Checking like appears under review')

    assert_match(response.updated[0].likes_count, expected_cnt, 'likes cnt')


@allure.step('Checking left review appears on page')
def assert_left_review_appears_on_page(response: GetReviewsRespSchema,
    expected_message: str,
    expected_email: str):

    logger.info('Checking left review appears on page')

    matched_review = next((review for review in response.data if review.author == expected_email),
        None)

    assert_match(matched_review.author, expected_email, 'email')
    assert_match(matched_review.message, expected_message, 'message')


