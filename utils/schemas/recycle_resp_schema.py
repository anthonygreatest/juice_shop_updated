from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field



class RecycleRespSchemaInside(BaseModel):

    is_pickup: Optional[bool] = Field(default=None, alias='isPickup')
    id: int
    user_id: int = Field(alias='UserId')
    address_id: int = Field(alias='AddressId')
    quantity: int
    updated_at: str = Field(alias='updatedAt')
    created_at: str = Field(alias='createdAt')
    date: Optional[datetime] = None

    model_config = {
        "populate_by_name": True
    }


class RecycleRespSchema(BaseModel):
    status: str
    data: RecycleRespSchemaInside

    model_config = {
        "populate_by_name": True
    }