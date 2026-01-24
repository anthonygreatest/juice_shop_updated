from pydantic import BaseModel, EmailStr


class LoginResponseSchemaInside(BaseModel):

    token: str
    bid: int
    umail: EmailStr

class LoginResponseSchema(BaseModel):

    authentication: LoginResponseSchemaInside