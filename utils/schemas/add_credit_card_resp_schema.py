from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

class AddCreditCardRespSchemaInside(BaseModel):

    id: int
    full_name: str = Field(alias='fullName')
    card_num: int = Field(alias='cardNum')
    exp_month: int = Field(alias='expMonth')
    exp_year: int = Field(alias='expYear')
    user_id: int = Field(alias='UserId')
    updated_at: datetime = Field(alias='updatedAt')
    created_at: datetime = Field(alias='createdAt')

    model_config = {
        "populate_by_name": True
    }

class AddCreditCardRespSchema(BaseModel):
    data: AddCreditCardRespSchemaInside
    status: str

    model_config = {
        "populate_by_name": True
    }

class GetCreditCardsRespSchemaInside(BaseModel):
    id: int
    full_name: str = Field(alias='fullName')
    card_num: str = Field(alias='cardNum')
    exp_month: int = Field(alias='expMonth')
    exp_year: int = Field(alias='expYear')
    user_id: int = Field(alias='UserId')

    model_config = {
        "populate_by_name": True
    }

class GetCreditCardsRespSchema(BaseModel):
    data: List[GetCreditCardsRespSchemaInside]
    status: str

    model_config = {
        "populate_by_name": True
    }

class DeleteCreditCardsRespSchema(BaseModel):
    data: str
    status: str

    model_config = {
        "populate_by_name": True
    }


