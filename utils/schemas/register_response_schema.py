from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class BaseRegistrationRespSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    deluxe_token: str = Field(alias='deluxeToken')
    last_login_ip: str = Field(alias='lastLoginIp')
    profile_image: str = Field(alias='profileImage')
    is_active: bool = Field(alias='isActive')
    updated_at: datetime = Field(alias='updatedAt')
    created_at: datetime = Field(alias='createdAt')
    deleted_at: None = Field(alias='deletedAt')

    model_config = {
        "populate_by_name": True
    }


class RegisterResponseValidateSchemaInside(BaseRegistrationRespSchema):
    pass

class RegisterResponseValidateSchema(BaseModel):

    status: str
    data: RegisterResponseValidateSchemaInside

    model_config = {
        "populate_by_name": True
    }



