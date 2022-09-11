from asyncio import Task
from typing import List
from pydantic import BaseModel

class Loop(BaseModel):
    freq: int
    task: Task
    tags: List[str]

    # Needed for Task type
    class Config:
        arbitrary_types_allowed = True