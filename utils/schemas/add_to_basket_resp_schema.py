from pydantic import Field
from datetime import datetime

from pydantic import BaseModel


class ProductInBasketSchema(BaseModel):
    status: str
    data: dict

class AddToBasketRespSchemaInside(BaseModel):

    id: int
    product_id: int = Field(alias='ProductId')
    basket_id: str | int = Field(alias='BasketId')
    quantity: int
    updated_at: datetime = Field(alias='updatedAt')
    created_at: datetime = Field(alias='createdAt')


    model_config = {
        "populate_by_name": True
    }


class AddToBasketRespSchema(ProductInBasketSchema):
    status: str
    data: AddToBasketRespSchemaInside

    model_config = {
        "populate_by_name": True
    }