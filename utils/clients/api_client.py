import json
from typing import Any

import allure
from httpx import Client, URL, QueryParams, Response
import requests

from config import HTTPClientConfig, Settings
from data.endpoints import Endpoints
from utils.schemas.add_address_resp_schema import AddAddressRespSchema, GetAddressesRespSchema
from utils.schemas.add_credit_card_resp_schema import AddCreditCardRespSchema, GetCreditCardsRespSchema
from utils.schemas.add_to_basket_resp_schema import AddToBasketRespSchema
from utils.schemas.captcha_resp_schema import CaptchaRespSchema, CaptchaDataErasureRespSchema
from utils.schemas.checkout_resp_schema import CheckoutRespSchema
from utils.schemas.data_export_resp_schema import DataExportRespSchema
from utils.schemas.digital_wallet_resp_schema import DigitalWalletRespSchema
from utils.schemas.existing_credit_card_schema import ExistingCreditCardSchema
from utils.schemas.get_all_products_in_basket_schema import GetAllProductsInBasketSchema
from utils.schemas.saved_pics_resp_schema import SavedPicsRespSchema
from utils.schemas.send_complaint_resp_schema import SendComplaintRespSchema
from utils.schemas.send_feedback_resp_schema import FeedbackRespSchema
from utils.schemas.upload_photo_resp_schema import UploadPhotoRespSchema

class BaseClient:

    def __init__(self, client: Client):
        self.client = client
        self.endpoints = Endpoints()

    def get(self,
            url: URL | str,
            headers: Any | None = None,
            params: QueryParams | None =None
        ) -> Response:
        return self.client.get(
            url=url,
            params=params,
            headers=headers
        )

    def post(self,
             url: URL | str,
             headers: Any | None = None,
             json: Any | None = None,
             data: Any | None = None,
             files: Any | None = None
        ) -> Response:
        return self.client.post(
            url=url,
            json=json,
            data=data,
            headers=headers,
            files=files
        )

    def put(self,
             url: URL | str,
             headers: Any | None = None,
             json: Any | None = None,
            data: Any | None = None,
        ) -> Response:
        return self.client.put(
            url=url,
            json=json,
            data=data,
            headers=headers
        )

    def delete(self,
             url: URL | str,
             headers: Any | None = None
        ) -> Response:
        return self.client.delete(
            url=url,
            headers=headers
        )


class Register(BaseClient):

    @allure.step('Sending register user request')
    def register_new_user(self, data) -> Response:
        return self.post(
            url=self.endpoints.register,
            json=data.model_dump(by_alias=True, mode='json')
        )

    @allure.step('Sending security answer request')
    def set_security_answer(self, data) -> Response:
        return self.post(
            url=self.endpoints.security_answer,
            json=data.model_dump(by_alias=True, mode='json')
        )

class Login(BaseClient):

    @allure.step('Sending login request')
    def log_in_user(self, data):
        return self.post(
            url=self.endpoints.login,
            json=data.model_dump(by_alias=True, mode='json')
        )

class ChangePassword(BaseClient):

    @allure.step('Sending change password request')
    def change_password(self, data) -> Response:
        return self.post(
            url=self.endpoints.change_password,
            json=data.model_dump(by_alias=True, mode='json')
        )

    @allure.step('Sending change password in account request')
    def change_password_in_account(self, params, headers=None) -> Response:
        return self.get(
            url=self.endpoints.change_password_in_account,
            params=params,
            headers=headers
        )

class CustomerFeedback(BaseClient):

    @allure.step('Sending post feedback request')
    def send_feedback(self, data, headers=None):
        return self.post(
            url=self.endpoints.feedback,
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers
        )

    @allure.step('Getting all feedback')
    def get_feedback(self, headers=None):
        response = self.get(
            url=self.endpoints.feedback,
            headers=headers
        )
        return FeedbackRespSchema(**response.json())

    @allure.step('Getting captcha')
    def get_captcha(self, headers=None) -> CaptchaRespSchema:
        resp = self.get(
            url=self.endpoints.captcha,
            headers=headers
        )
        return CaptchaRespSchema(**resp.json())

class Basket(BaseClient):

    @allure.step('Sending add product to basket request')
    def add_to_basket(self, data, headers=None):
        return self.post(
            url=self.endpoints.add_to_basket,
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers
        )

    @allure.step('Sending change product quantity in basket request')
    #здесь раньше был трай иксепт
    def change_product_quantity(self, order_id, data, headers=None):
        return self.put(
            url=f'{self.endpoints.add_to_basket}/{order_id}',
            json=data,
            headers=headers
        )

    @allure.step('Sending delete product from basket request')
    def delete_product_from_basket(self, order_id, headers=None):
        return self.delete(
            url=f'{self.endpoints.add_to_basket}/{order_id}',
            headers=headers
        )

    @allure.step('Getting all products in basket')
    def get_all_products_in_basket(self, order_id, headers=None):
        response = self.get(
            url=f'{self.endpoints.basket}/{order_id}',
            headers=headers
        )
        return GetAllProductsInBasketSchema(**response.json())

class Address(BaseClient):

    @allure.step('Sending add address request')
    def create_address(self, data, headers=None):
        return self.post(
            url=self.endpoints.add_address,
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers
        )

    @allure.step('Getting all addresses')
    def get_addresses(self, headers=None):
        resp = self.get(
            url=self.endpoints.add_address,
            headers=headers
        )
        return GetAddressesRespSchema(**resp.json())

    @allure.step('Sending change address request')
    def change_address(self, data, address_id, headers=None):
        return self.put(
            url=f'{self.endpoints.add_address}/{address_id}',
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers,
        )

    @allure.step('Sending delete address request')
    def delete_address(self, address_id, headers=None):
        return self.delete(
            url=f'{self.endpoints.add_address}/{address_id}',
            headers=headers
        )

class DeliveryOptions(BaseClient):

    @allure.step('Sending delivery option request')
    def choose_delivery(self, option, headers=None):
        return self.get(
            url=f'{self.endpoints.delivery_options}/{option}',
            headers=headers
        )

    @allure.step('Getting delivery options')
    def get_delivery_options(self, headers):
        return self.get(
            url=self.endpoints.delivery_options,
            headers=headers
        )

class CreditCard(BaseClient):

    @allure.step('Sending add credit card request')
    def add_credit_card(self, data, headers=None):

        return self.post(
            url=self.endpoints.credit_card,
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers
        )

    @allure.step('Getting all credit cards')
    def get_credit_cards(self, headers=None):
        response = self.get(
            url=self.endpoints.credit_card,
            headers=headers
        )
        return GetCreditCardsRespSchema(**response.json())

    @allure.step('Sending delete credit card request')
    def delete_credit_card(self, card_id, headers=None):
        return self.delete(
            url=f'{self.endpoints.credit_card}/{card_id}',
            headers=headers
        )

class Checkout(BaseClient):

    @allure.step('Sending checkout request')
    def make_order_at_checkout(self, data, basket_id, headers=None):
        return self.post(
            url=f'{self.endpoints.checkout(basket_id)}',
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers
        )

class TrackingOrder(BaseClient):

    @allure.step('Getting tracking order')
    def get_tracking_order(self, tracking_id, headers=None):
        return self.get(
            url=f'{self.endpoints.tracking}/{tracking_id}',
            headers=headers
        )

class OrderHistory(BaseClient):

    @allure.step('Getting order history')
    def get_order_history(self, headers=None):
        return self.get(
            url=self.endpoints.order_history,
            headers=headers
        )
class Recycle(BaseClient):

    @allure.step('Sending recycle request')
    def recycle(self, data, headers=None):
        return self.post(
            url=self.endpoints.recycle,
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers
        )

class DigitalWallet(BaseClient):

    @allure.step('Sending deposit request')
    def deposit_to_digital_wallet(self, data, headers=None):
        return self.put(
            url=self.endpoints.digital_wallet,
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers
        )

    @allure.step('Getting digital wallet balance')
    def get_digital_wallet_balance(self, headers=None):
        resp =  self.get(
            url=f'{self.endpoints.digital_wallet}',
            headers=headers
        )

        return DigitalWalletRespSchema(**resp.json())

class DataExport(BaseClient):

    @allure.step('Sending data export request')
    def request_data_export(self, data, headers=None):
        return self.post(
            url=self.endpoints.data_export,
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers
        )

    @allure.step('Getting captcha')
    def request_captcha(self, headers=None):
        resp = self.get(
            url=self.endpoints.data_export_captcha,
            headers=headers
        )
        return CaptchaDataErasureRespSchema(**resp.json())

class DeluxeMembership(BaseClient):

    @allure.step('Sending deluxe membership request')
    def become_deluxe_member(self, data, headers=None):
        return self.post(
            url=self.endpoints.deluxe_membership,
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers
        )

class Complaints(BaseClient):

    @allure.step('Sending complaint request')
    def file_a_complaint(self, data, headers=None):
        return self.post(
            url=self.endpoints.complaint,
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers
        )

class PhotoWall(BaseClient):

    @allure.step('Sending upload photo request')
    def upload_photo(self, files, data=None, headers=None):
        return self.post(
            url=self.endpoints.photo_wall,
            headers=headers,
            files=files,
            data=data
        )

    @allure.step('Getting all photos')
    def get_photos(self, headers=None):
        response = self.get(
            url=self.endpoints.photo_wall,
            headers=headers
        )
        return SavedPicsRespSchema(**response.json())

class Chatbot(BaseClient):

    @allure.step('Sending chatbot query')
    def ask_robot(self, data, headers=None):
        return self.post(
            url=self.endpoints.robot,
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers
        )

    @allure.step('Getting welcome message from chatbot')
    def get_welcome_message(self, headers):
        return self.get(
            url=self.endpoints.robot,
            headers=headers
        )

class Logout(BaseClient):

    @allure.step('Sending logout request')
    def log_out_user(self, headers=None):
        return self.get(
            url=self.endpoints.logout,
            headers=headers
        )


class Reviews(BaseClient):

    @allure.step('Getting reviews')
    def get_reviews(self, product_id, headers):
        return self.get(
            url=self.endpoints.all_reviews(product_id),
            headers=headers
        )

    @allure.step('Sending write review request')
    def write_review(self, data, product_id, headers):
        return self.put(
            url=self.endpoints.all_reviews(product_id),
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers
        )

    @allure.step('Sending like review request')
    def like_a_review(self, data, headers):
        return self.post(
            url=self.endpoints.reviews,
            json=data.model_dump(by_alias=True, mode='json'),
            headers=headers
        )

class DataErasure(BaseClient):

    @allure.step('Sending data erasure request')
    def request_data_erasure(self, data, headers=None):
        return self.post(
            url=self.endpoints.data_erasure,
            data=data,
            headers=headers
        )
