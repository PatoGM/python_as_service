import asyncio
import os
import psutil
from fastapi import APIRouter, WebSocket

router = APIRouter(
    prefix="/home",
)

@router.get("")
async def pasta():
    return {"pasta": "is delicious"}

psutil.cpu_percent()

@router.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            await websocket.send_json({"cpu": psutil.cpu_percent()})
            await websocket.send_json({"ram": psutil.virtual_memory()[2]})
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            break

@router.get("/fs/{file_path:path}")
async def get_stats(file_path: str):
    base = "C:/"
    path = base + file_path
    print(path)

    for subdir, dirs, files in os.walk(path):
        print(subdir, dirs, files)
        return dirs, files
    
    print("FILE or NO ACCESS")
    return os.lstat(path)