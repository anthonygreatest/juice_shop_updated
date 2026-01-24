from dataclasses import dataclass
from decimal import Decimal


@dataclass
class DeliveryData:

    delivery_price: Decimal
    delivery_date: int