from dataclasses import dataclass

from data.dataclasses.delivery_data import DeliveryData
from data.dataclasses.e_wallet_deposit_data import EWalletDepositData
from data.dataclasses.selected_product_data import SelectedProductData
from utils.schemas.add_address_request_schema import AddAddressSchema
from utils.schemas.add_credit_card_request import AddCreditCardRequest


@dataclass
class SetOrderData:
    selected_product_data: SelectedProductData
    address_data: AddAddressSchema
    card_data: AddCreditCardRequest
    delivery_data: DeliveryData
    deposit_data: EWalletDepositData