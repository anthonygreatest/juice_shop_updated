from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel


class RecycleRequestSchema(BaseModel):

    user_id: int = Field(alias='UserId')
    address_id: int = Field(alias='AddressId')
    quantity: int
    date: Optional[datetime] = None
    is_pickup: Optional[bool] = Field(default=None, alias='isPickup')

    model_config = {
        "populate_by_name": True
    }
