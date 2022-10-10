import uvicorn
from global_variables import GLOBAL_VARIABLES

from app import app as MAIN_APP

if __name__ == "__main__":
    if (GLOBAL_VARIABLES is None):
        print("Error: Cannot read settings.json or whatever file holds the global variables")
    else:
        try:
            # uvicorn.run("app:app", reload=GLOBAL_VARIABLES.debug, host=GLOBAL_VARIABLES.host, port=GLOBAL_VARIABLES.port)
            uvicorn.run("app:app", reload=GLOBAL_VARIABLES.debug, host=GLOBAL_VARIABLES.host, port=GLOBAL_VARIABLES.port, log_level="info")
        except Exception as e:
            print(e)