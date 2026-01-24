from enum import Enum

from pydantic import BaseModel, EmailStr, field_validator


class UserErrors(Enum):

    WRONG_PASSWORD = 'Password is not valid'
    WRONG_CARD_LENGTH = 'Card number length is not valid'
    UNPROTECTED_CARD_NUMBER = 'Card number is not ciphered'


class RandomPasswordSchema(BaseModel):

    answer: str | int
    email: EmailStr
    new: str
    repeat: str

    @field_validator('new')
    def validate_email(cls, new):
        if 0 < len(new) <= 20:
            return new
        else:
            raise ValueError(UserErrors.WRONG_PASSWORD.value)

