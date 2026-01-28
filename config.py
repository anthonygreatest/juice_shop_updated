from pathlib import Path

from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class HTTPClientConfig(BaseModel):

    url: HttpUrl
    timeout: float

    @property
    def client_url(self) -> str:
        return str(self.url)

BASE_DIR = Path(__file__).parent

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__'
    )

    shop_http_client: HTTPClientConfig

# settings = Settings()
#
# print(settings.shop_http_client.url)
# print(settings.shop_http_client.timeout)