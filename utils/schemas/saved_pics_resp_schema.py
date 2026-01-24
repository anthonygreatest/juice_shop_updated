from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from utils.schemas.register_response_schema import BaseRegistrationRespSchema


class SavedPicsRespSchemaInside(BaseModel):

    user_id: int = Field(alias='UserId')
    id: int
    caption: Optional[str] = None
    image_path: str = Field(alias='imagePath')
    created_at: datetime = Field(alias='createdAt')
    updated_at: datetime = Field(alias='updatedAt')
    user: BaseRegistrationRespSchema = Field(alias='User')

    model_config = {
        "populate_by_name": True
    }

class SavedPicsRespSchema(BaseModel):

    status: str
    data: List[SavedPicsRespSchemaInside]

    model_config = {
        "populate_by_name": True
    }