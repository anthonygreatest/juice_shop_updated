from pydantic import Field, BaseModel

from utils.schemas.register_response_schema import BaseRegistrationRespSchema


class ChangePasswordRespSchemaInside(BaseRegistrationRespSchema):

    password: str
    totp_secret: str = Field(alias='totpSecret')

    model_config = {
        "populate_by_name": True
    }


class ChangePasswordRespSchema(BaseModel):
    user: ChangePasswordRespSchemaInside
