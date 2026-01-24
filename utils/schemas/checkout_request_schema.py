from typing import Optional

from pydantic import BaseModel, Field


class CheckoutRequestSchemaInside(BaseModel):

    address_id: str = Field(alias='addressId')
    delivery_method_id: str = Field(alias='deliveryMethodId')
    payment_id: str = Field(alias='paymentId')

    model_config = {
        "populate_by_name": True
    }

class CheckoutRequestSchema(BaseModel):
    coupon_data: Optional[str] = Field(alias='couponData')
    order_details: CheckoutRequestSchemaInside = Field(alias='orderDetails')

    model_config = {
        "populate_by_name": True
    }
