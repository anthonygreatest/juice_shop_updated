from decimal import Decimal

from pydantic import BaseModel, Field


class DigitalWalletRequestSchema(BaseModel):

    balance: Decimal
    payment_id: str | int = Field(alias='paymentId')

    model_config = {
        "populate_by_name": True
    }
