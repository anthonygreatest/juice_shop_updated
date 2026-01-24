from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from utils.schemas.add_to_basket_resp_schema import AddToBasketRespSchemaInside, ProductInBasketSchema


class ProductsInBasketSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float | int
    deluxe_price: float | int = Field(alias='deluxePrice')
    image: str
    updated_at: datetime = Field(alias='updatedAt')
    created_at: datetime = Field(alias='createdAt')
    deleted_at: datetime | None = Field(alias='deletedAt')
    basket_item: AddToBasketRespSchemaInside = Field(alias='BasketItem')

    model_config = {
        "populate_by_name": True
    }

class GetAllProductsInBasketSchemaInside(BaseModel):
    id: int
    coupon: str | None
    user_id: int = Field(alias='UserId')
    updated_at: datetime = Field(alias='updatedAt')
    created_at: datetime = Field(alias='createdAt')
    products: List[ProductsInBasketSchema] = Field(alias='Products')


    model_config = {
        "populate_by_name": True
    }

class GetAllProductsInBasketSchema(ProductInBasketSchema):
    status: str
    data: GetAllProductsInBasketSchemaInside

