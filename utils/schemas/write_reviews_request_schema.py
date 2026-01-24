from pydantic import BaseModel, EmailStr


class WriteReviewsRequestSchema(BaseModel):

    author: EmailStr
    message: str


class WriteReviewsRespSchema(BaseModel):

    status: str