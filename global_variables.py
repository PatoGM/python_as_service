import json
from pydantic import BaseModel

settings_file = "./settings.json"

class Global_Variables(BaseModel):
    host: str
    port: int
    opc_url: str
    opc_idx: str
    debug: bool

try:
    with open(settings_file) as f:
        GLOBAL_VARIABLES = Global_Variables.parse_obj(json.load(f))
except Exception as e:
    GLOBAL_VARIABLES = None