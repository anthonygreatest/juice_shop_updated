from pydantic import BaseModel

class DeluxeRespSchemaInside(BaseModel):
    confirmation: str
    token: str

    model_config = {
        "populate_by_name": True
    }


class DeluxeRespSchema(BaseModel):
    status: str
    data: DeluxeRespSchemaInside

    model_config = {
        "populate_by_name": True
    }