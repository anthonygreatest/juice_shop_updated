from datetime import datetime

from pydantic import BaseModel, Field


class UploadPhotoRespSchemaInside(BaseModel):
    id: int
    caption: str
    image_path: str = Field(alias='imagePath')
    user_id: int = Field(alias='UserId')
    updated_at: datetime = Field(alias='updatedAt')
    created_at: datetime = Field(alias='createdAt')

    model_config = {
        "populate_by_name": True
    }


class UploadPhotoRespSchema(BaseModel):

    status: str
    data: UploadPhotoRespSchemaInside

    model_config = {
        "populate_by_name": True
    }
