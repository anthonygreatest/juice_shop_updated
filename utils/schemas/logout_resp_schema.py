from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LogoutRespSchema(BaseModel):

    id: int
    username: str | None
    email: EmailStr
    password: str
    role: str
    deluxe_token: str | None = Field(alias='deluxeToken')
    last_login_ip: str | None = Field(alias='lastLoginIp')
    profile_image: str = Field(alias='profileImage')
    totp_secret: str | None = Field(alias='totpSecret')
    is_active: bool = Field(alias='isActive')
    created_at: datetime = Field(alias='createdAt')
    updated_at: datetime = Field(alias='updatedAt')
    deleted_at: datetime | None = Field('deletedAt')

    model_config = {
        "populate_by_name": True
    }