from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SendFeedbackGenRespSchema(BaseModel):

    id: int
    user_id: int | None = Field(alias='UserId')
    updated_at: datetime = Field(alias='updatedAt')
    created_at: datetime = Field(alias='createdAt')

    model_config = {
        "populate_by_name": True
    }


class SendComplaintRespSchemaInside(SendFeedbackGenRespSchema):

    message: str | None
    file: str | None

    model_config = {
        "populate_by_name": True
    }

class SendComplaintRespSchema(BaseModel):

    status: str
    data: SendComplaintRespSchemaInside

    model_config = {
        "populate_by_name": True
    }
