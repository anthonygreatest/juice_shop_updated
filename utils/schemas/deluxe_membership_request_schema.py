from typing import Optional

from pydantic import BaseModel, Field


class DeluxeRequestSchema(BaseModel):
    payment_id: Optional[int] = Field(default=None, alias='paymentId')
    payment_mode: str = Field(alias='paymentMode')

    model_config = {
        "populate_by_name": True
    }
