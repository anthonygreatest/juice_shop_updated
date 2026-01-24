from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

class RegisterRequestSchemaSecurity(BaseModel):
    id: int
    question: str
    created_at: datetime = Field(alias='createdAt')
    updated_at: datetime = Field(alias='updatedAt')


    model_config = {
        "populate_by_name": True
    }

class RegisterRequestSchema(BaseModel):
    email: EmailStr
    password: str
    password_repeat: str = Field(alias='passwordRepeat')
    security_question: RegisterRequestSchemaSecurity = Field(alias='securityQuestion')
    security_answer: str | int = Field(alias='securityAnswer')


    model_config = {
        "populate_by_name": True
    }