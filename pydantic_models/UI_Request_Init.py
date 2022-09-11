from typing import List
from pydantic import BaseModel, validator

INIT_TYPE = "OPC_PLC_INIT"

class UI_Request_Init(BaseModel):
    Type: str
    Tag: List[str]

    @validator("Type")
    def correct_type(cls, value):
        if value != INIT_TYPE:
            raise ValueError("Type must be " + INIT_TYPE)
        return value