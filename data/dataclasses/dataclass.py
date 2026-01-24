from dataclasses import dataclass

from utils.schemas.get_reviews_resp_schema import GetReviewsRespSchema


@dataclass
class UnlikedReview:
    selected_product_reviews: GetReviewsRespSchema
    comment_to_like: str
    product_id: int | str
    num_of_likes: int
