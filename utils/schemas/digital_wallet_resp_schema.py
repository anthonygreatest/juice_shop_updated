from decimal import Decimal

from pydantic import BaseModel


class DigitalWalletRespSchema(BaseModel):

    data: Decimal
    status: str