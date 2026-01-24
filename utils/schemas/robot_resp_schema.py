from pydantic import BaseModel


class RobotRespSchema(BaseModel):

    action: str
    body: str

class RobotRequestSchema(BaseModel):

    action: str
    query: str
