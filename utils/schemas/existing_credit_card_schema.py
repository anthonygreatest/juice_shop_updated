from typing import List

from pydantic import BaseModel, Field, field_validator

from utils.schemas.password_schema import UserErrors


class ExistingCreditCardSchemaInside(BaseModel):
    user_id: int = Field(alias='UserId')
    id: int
    full_name: str = Field(alias='fullName')
    card_num: str = Field(alias='cardNum')
    exp_month: int = Field(alias='expMonth')
    exp_year: int = Field(alias='expYear')

    @field_validator('card_num')
    def card_validator(cls, card_num):
        if len(card_num) == 16 and card_num[:12] == '*' * 12 and card_num[12:].isdigit():
            return card_num
        else:
            raise ValueError(UserErrors.UNPROTECTED_CARD_NUMBER.value)



class ExistingCreditCardSchema(BaseModel):
    status: str
    data: List[ExistingCreditCardSchemaInside]