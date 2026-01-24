from datetime import datetime

from pydantic import Field, BaseModel


class DataErasureRequestSchema(BaseModel):

    email: str
    security_answer: str | int | datetime = Field(alias='securityAnswer')