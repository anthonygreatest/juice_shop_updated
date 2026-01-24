import random
from http import HTTPStatus

import allure

from utils.assertions.base_assertions import assert_status_code
from utils.assertions.review_assertions import assert_like_gets_added, assert_like_appears_under_review, \
    assert_left_review_appears_on_page
from utils.helper import get_product_reviews
from utils.schemas.like_review_resp_schema import LikeReviewRespSchema
from utils.schemas.write_reviews_request_schema import WriteReviewsRespSchema
from utils.validators import validate_response


@allure.feature('Reviews')
@allure.story('Valid review flow')
class TestReviews:

    @allure.title('User able to leave a like')
    def test_like_appears_on_page(self, leave_a_like_under_review, login_response):

        response = leave_a_like_under_review

        validated_response = validate_response(LikeReviewRespSchema, response.json())

        assert_status_code(response, HTTPStatus.OK)
        assert_like_gets_added(validated_response, login_response.authentication.umail)


    @allure.title('Like appears under review')
    def test_number_of_likes(self, leave_a_like_under_review, get_unliked_review):

        likes_before = get_unliked_review.num_of_likes

        response = leave_a_like_under_review
        validated_response = validate_response(LikeReviewRespSchema, response.json())

        assert_like_appears_under_review(validated_response, likes_before + 1)


    @allure.title('User able to write reviews')
    def test_user_able_to_write_reviews(self, reviews, headers_with_auth, write_review):

        response = write_review.response

        validate_response(WriteReviewsRespSchema, response.json())

        assert_status_code(response, HTTPStatus.CREATED)


    @allure.title('Left review appears in product card')
    def test_left_review_appears_on_page(self, write_review, headers_with_auth, reviews):

        reviewed_product = write_review.reviewed_product
        reviewer_email = write_review.email
        review_message = write_review.message

        selected_product_reviews = get_product_reviews(
            reviews=reviews,
            headers=headers_with_auth,
            product=reviewed_product
        )

        assert_left_review_appears_on_page(
            response=selected_product_reviews,
            expected_email=reviewer_email,
            expected_message=review_message
        )






