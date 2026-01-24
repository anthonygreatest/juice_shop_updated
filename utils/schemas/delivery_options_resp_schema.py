from decimal import Decimal
from typing import List

from pydantic import BaseModel


class DeliveryOptionsRespSchemaInside(BaseModel):

    id: int
    name: str
    price: Decimal
    eta: int
    icon: str

class DeliveryOptionsRespSchema(BaseModel):
    status: str
    data: DeliveryOptionsRespSchemaInside