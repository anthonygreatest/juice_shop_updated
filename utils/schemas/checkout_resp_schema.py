from pydantic import BaseModel, Field


class CheckoutRespSchema(BaseModel):

    order_confirmation: str = Field(alias='orderConfirmation')

    model_config = {
        "populate_by_name": True
    }
