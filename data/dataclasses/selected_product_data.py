from dataclasses import dataclass
from decimal import Decimal


@dataclass
class SelectedProductData:
    product_name: str
    product_price: Decimal

