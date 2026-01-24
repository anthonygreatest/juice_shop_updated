from dataclasses import dataclass

from httpx import Response

from utils.schemas.digital_wallet_request_schema import DigitalWalletRequestSchema
from utils.schemas.digital_wallet_resp_schema import DigitalWalletRespSchema


@dataclass
class EWalletDepositData:

    response_raw: Response
    deposit_payload: DigitalWalletRequestSchema
    balance_before_deposit: DigitalWalletRespSchema