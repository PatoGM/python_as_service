from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import routers.home
import routers.uiredesign

app = FastAPI()

# Serve static files / GUI
app.mount("/gui", StaticFiles(directory="static", html=True), name="static")

# Add all routers to app
app.include_router(routers.home.router)
app.include_router(routers.uiredesign.router)
