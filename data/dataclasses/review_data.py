from dataclasses import dataclass

from httpx import Response
from pydantic import EmailStr

from utils.schemas.write_reviews_request_schema import WriteReviewsRequestSchema


@dataclass
class ReviewData:
    response: Response
    email: EmailStr
    reviewed_product: str
    message: WriteReviewsRequestSchema

