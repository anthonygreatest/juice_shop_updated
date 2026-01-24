from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


class GetReviewsRespGenericSchema(BaseModel):

    message: Optional[str] = None
    author: Optional[EmailStr] = None
    product: int
    likes_count: int = Field(alias='likesCount')
    liked_by: List[str] = Field(alias='likedBy')
    id: str = Field(alias='_id')

    model_config = {
        "populate_by_name": True
    }

    @model_validator(mode='before')
    @classmethod
    def empty_str_to_none(cls, values: dict):
        for field in ['author', 'email']:
            if field in values and values[field] == "":
                values[field] = None
            return values


class GetReviewsRespSchemaInside(GetReviewsRespGenericSchema):

    # liked: Optional[bool]

    model_config = {
        "populate_by_name": True
    }

class GetReviewsRespSchema(BaseModel):

    status: str
    data: List[GetReviewsRespSchemaInside]

    model_config = {
        "populate_by_name": True
    }