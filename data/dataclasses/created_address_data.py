from dataclasses import dataclass

from httpx import Response

from utils.schemas.add_address_request_schema import AddAddressSchema
from utils.schemas.add_address_resp_schema import AddAddressRespSchema


@dataclass
class CreatedAddressData:

    response_raw: Response
    address_payload: AddAddressSchema
    added_address: AddAddressRespSchema