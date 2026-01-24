from dataclasses import dataclass

from httpx import Response

from utils.schemas.add_credit_card_request import AddCreditCardRequest
from utils.schemas.add_credit_card_resp_schema import AddCreditCardRespSchema


@dataclass
class CreatedCardData:

    response_raw: Response
    card_payload: AddCreditCardRequest
    added_card: AddCreditCardRespSchema