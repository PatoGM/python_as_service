from typing import Dict, List
from pydantic import BaseModel
from pydantic_models.tag_group import Tag_Group

class Tag_Request(BaseModel):
    Read: List[Tag_Group] = []
    Write: Dict[str, str] = {}