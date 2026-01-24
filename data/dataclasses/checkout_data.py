from dataclasses import dataclass

from httpx import Response

from data.dataclasses.selected_product_data import SelectedProductData
from utils.schemas.add_address_resp_schema import AddAddressRespSchema
from utils.schemas.add_credit_card_resp_schema import AddCreditCardRespSchema
from utils.schemas.add_to_basket_request_schema import AddToBasketRequestSchema
from utils.schemas.delivery_options_resp_schema import DeliveryOptionsRespSchema
from utils.schemas.digital_wallet_resp_schema import DigitalWalletRespSchema


@dataclass
class CheckoutData:
    checkout_response: Response
    balance_before: DigitalWalletRespSchema
    selected_product: AddToBasketRequestSchema
    address_created: AddAddressRespSchema
    card_created: AddCreditCardRespSchema
    delivery_selected: DeliveryOptionsRespSchema
    product_name_and_price: SelectedProductData

