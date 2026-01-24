from pydantic import BaseModel, Field


class SetSecuritySchema(BaseModel):

    user_id: int | str = Field(alias='UserId')
    answer: str
    security_question_id: int | str = Field(alias='SecurityQuestionId')


    model_config = {
        "populate_by_name": True
    }
