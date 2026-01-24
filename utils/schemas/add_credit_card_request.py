from pydantic import BaseModel, field_validator, Field

from utils.schemas.password_schema import UserErrors


class AddCreditCardRequest(BaseModel):

    full_name: str = Field(alias='fullName')
    card_num: int = Field(alias='cardNum')
    exp_month: str = Field(alias='expMonth')
    exp_year: str = Field(alias='expYear')

    model_config = {
        "populate_by_name": True
    }

    @field_validator('card_num')
    def validate_card_length(cls, card_num):
        if len(str(card_num)) == 16:
            return card_num
        else:
            raise ValueError(UserErrors.WRONG_CARD_LENGTH.value)
