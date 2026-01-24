from typing import Optional

from pydantic import BaseModel, Field


class SendFeedbackGenRequestSchema(BaseModel):
    user_id: Optional[int] = Field(alias='UserId')

    model_config = {
        "populate_by_name": True
    }


class SendFeedbackRequestSchema(SendFeedbackGenRequestSchema):

    captcha: Optional [str | int]
    captcha_id: Optional [int | str] = Field(alias='captchaId')
    comment: str
    rating: str | int

    model_config = {
        "populate_by_name": True
    }