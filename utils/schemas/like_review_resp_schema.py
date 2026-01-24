from typing import List

from pydantic import BaseModel

from utils.schemas.get_reviews_resp_schema import GetReviewsRespGenericSchema


class LikeReviewRespSchema(BaseModel):

    modified: int
    original: List[GetReviewsRespGenericSchema]
    updated: List[GetReviewsRespGenericSchema]

class LikeReviewRequestSchema(BaseModel):

    id: str