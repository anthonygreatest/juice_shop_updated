from typing import List, Optional
from decimal import Decimal

from pydantic import BaseModel, Field

class DataExportRespSchemaProducts(BaseModel):

    quantity: int
    id: int
    name: str
    price: int | float
    total: int | float
    bonus: int | float

class DataExportRespSchemaOrders(BaseModel):

    order_id: str = Field(alias='orderId')
    total_price: int | float | Decimal = Field(alias='totalPrice')
    products: List[DataExportRespSchemaProducts]
    bonus: int | float
    eta: int | str

    model_config = {
        "populate_by_name": True
    }



class DataExportRespSchemaInside(BaseModel):

    username: str
    email: str
    orders: List[DataExportRespSchemaOrders]

    model_config = {
        "populate_by_name": True
    }


class DataExportRespSchema(BaseModel):

    user_data: DataExportRespSchemaInside | str = Field(alias='userData')
    confirmation: str

    model_config = {
        "populate_by_name": True
    }

class DataExportRequestSchema(BaseModel):

    format: str
    answer: Optional[str] = None
