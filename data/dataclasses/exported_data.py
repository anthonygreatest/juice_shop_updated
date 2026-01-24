from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ExportedData:

    name: str
    total_price: Decimal
    order_id: str
    delivery_date: int
