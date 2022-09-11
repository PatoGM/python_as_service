from typing import List
from pydantic import BaseModel

class Tag_Group(BaseModel):
    Interval_ms: int = 1000
    Tags: List[str] = []