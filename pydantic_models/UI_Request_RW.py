from pydantic import BaseModel, validator
from pydantic_models.tag_request import Tag_Request

RW_TYPE = "PLC_RW"
RW_DESTINATION = "PLC/IPC"

class UI_Request_RW(BaseModel):
    Type: str
    Destination: str
    Request: Tag_Request

    @validator("Type")
    def correct_type(cls, value):
        if value != RW_TYPE:
            raise ValueError("Type must be " + RW_TYPE)
        return value

    @validator("Destination")
    def correct_destination(cls, value):
        if value != RW_DESTINATION:
            raise ValueError("Destination must be " + RW_DESTINATION)
        return value