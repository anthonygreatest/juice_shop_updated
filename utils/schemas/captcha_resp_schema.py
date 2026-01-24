from pydantic import BaseModel, Field


class CaptchaDataErasureRespSchema(BaseModel):
    user_id: int | str = Field(alias='UserId')
    image: str
    answer: str

    model_config = {
        "populate_by_name": True
    }

class CaptchaRespSchema(BaseModel):

    captcha_id: int | str = Field(alias='captchaId')
    captcha: str
    answer: str