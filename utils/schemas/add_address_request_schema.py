from typing import Optional

from pydantic import BaseModel, Field


class AddAddressSchema(BaseModel):

    city: str
    country: str
    full_name: str = Field(alias='fullName')
    mobile_num: int | str = Field(alias='mobileNum')
    zip_code: str = Field(alias='zipCode')
    street_address: str = Field(alias='streetAddress')
    state: Optional[str] = None

    model_config = {
        "populate_by_name": True
    }
