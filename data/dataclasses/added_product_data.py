from dataclasses import dataclass

from httpx import Response

from utils.schemas.add_to_basket_request_schema import AddToBasketRequestSchema
from utils.schemas.add_to_basket_resp_schema import AddToBasketRespSchemaInside


@dataclass
class AddedProductData:

    added_product: AddToBasketRequestSchema
    raw_response: Response
    item: AddToBasketRespSchemaInside | None