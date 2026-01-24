from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class ProductOrderSchema(BaseModel):
    quantity: int
    id: int
    name: str
    price: Decimal
    total: Decimal
    bonus: int | float

class GetOrderHistorySchema(BaseModel):
    promotional_amount: int | float | str = Field(alias='promotionalAmount')
    payment_id: str = Field(alias='paymentId')
    address_id: str = Field(alias='addressId')
    order_id: str = Field(alias='orderId')
    delivered: bool
    email: str
    total_price: Decimal = Field(alias='totalPrice')
    products: List[ProductOrderSchema]
    bonus: str | int | float
    delivery_price: Decimal = Field(alias='deliveryPrice')
    eta: str
    _id: str

    model_config = {
        "populate_by_name": True
    }


class GetOrderHistoryListSchema(BaseModel):
    status: str
    data: List[GetOrderHistorySchema]

    model_config = {
        "populate_by_name": True
    }
