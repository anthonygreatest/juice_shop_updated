
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class AddAddressRespSchemaInside(BaseModel):

    id: int
    city: str
    country: str
    full_name: str = Field(alias='fullName')
    mobile_num: int | str = Field(alias='mobileNum')
    zip_code: str = Field(alias='zipCode')
    street_address: str = Field(alias='streetAddress')
    state: Optional[str] = None
    user_id: int = Field(alias='UserId')
    updated_at: datetime = Field(alias='updatedAt')
    created_at: datetime = Field(alias='createdAt')

    model_config = {
        "populate_by_name": True
    }

class AddAddressRespSchema(BaseModel):
    status: str
    data: AddAddressRespSchemaInside

    model_config = {
        "populate_by_name": True
    }

class GetAddressesRespSchema(BaseModel):
    status: str
    data: List[AddAddressRespSchemaInside]

    model_config = {
        "populate_by_name": True
    }

class DeleteAddressRespSchema(BaseModel):
    status: str
    data: str

    model_config = {
        "populate_by_name": True
    }