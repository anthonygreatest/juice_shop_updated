from dataclasses import dataclass

from utils.schemas.login_response_schema import LoginResponseSchema
from utils.schemas.register_request_schema import RegisterRequestSchema
from utils.schemas.register_response_schema import RegisterResponseValidateSchema


@dataclass
class LoginData:
    headers_with_auth: dict
    register_response: RegisterResponseValidateSchema
    registered_user_data: RegisterRequestSchema
    login_response: LoginResponseSchema

