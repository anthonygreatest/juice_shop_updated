from typing import List

from pydantic import BaseModel

from utils.schemas.send_complaint_resp_schema import SendFeedbackGenRespSchema


class FeedbackRespSchemaInside(SendFeedbackGenRespSchema):

    comment: str
    rating: int

    model_config = {
        "populate_by_name": True
    }



class FeedbackRespSchema(BaseModel):
    status: str
    data: FeedbackRespSchemaInside | List[FeedbackRespSchemaInside]

    model_config = {
        "populate_by_name": True
    }
