from datetime import datetime

from pydantic import BaseModel, Field


class SecurityQuestionRespSchemaInside(BaseModel):

    id: int
    user_id: int | str = Field(alias='UserId')
    answer: str
    security_question_id: int | str = Field(alias='SecurityQuestionId')
    updated_at: datetime = Field(alias='updatedAt')
    created_at: datetime = Field(alias='createdAt')

    model_config = {
        "populate_by_name": True
    }

class SecurityQuestionRespSchema(BaseModel):

    status: str
    data: SecurityQuestionRespSchemaInside

    model_config = {
        "populate_by_name": True
    }
