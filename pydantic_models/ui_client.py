from typing import List
from fastapi import WebSocket
from pydantic import BaseModel
from pydantic_models.loop import Loop

class UI_Client(BaseModel):
    ws: WebSocket
    loops: List[Loop]

    # Needed for WebSocket type
    class Config:
        arbitrary_types_allowed = True