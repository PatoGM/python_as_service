import asyncio
import ntpath
import os
from sys import platform
from time import perf_counter
import psutil
from fastapi import APIRouter, WebSocket

PREFIX = "/home"

router = APIRouter(
    prefix=PREFIX,
)

psutil.cpu_percent()

http_endpoints = []
ws_endpoints = []

ws_endpoints.append("/ws")
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

# async def get_stats(file_path: str):
#     base = "C:/"
#     path = base + file_path
#     print(path)

#     for subdir, dirs, files in os.walk(path):
#         print(subdir, dirs, files)
#         return dirs, files
    
#     print("FILE or NO ACCESS")
#     return os.lstat(path)

# https://stackoverflow.com/questions/21455021/python-map-a-filesystem-to-a-directory-structure-works-but-how
http_endpoints.append("/fs, number, path")
@router.get("/fs/{max_depth}/{rootdir:path}")
async def get_directory_structure(max_depth: int, rootdir: str):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    rootdir = "/" + rootdir
    rootdir = rootdir.replace("/", os.path.sep)

    if platform != "win32":
        # Not Windows
        return {}
    elif platform == "win32":
        # Windows
        rootdir = "C:" + rootdir
        return get_directory_structure_to_some_depth(rootdir, perf_counter(), maxdepth=max_depth)

def get_directory_structure_to_some_depth(rootdir: str, start_time: float, depth: int = 0, maxdepth: int = 5):
    
    curr_time = perf_counter()
    dif = curr_time - start_time
    print(dif)
    # After 5 seconds of running, begin to timeout and end request ASAP
    if dif > 5:
        return None

    try:
        for path, subdirs, files in os.walk(rootdir):
            subdir_obj = dict.fromkeys(subdirs)

            for file in files:
                subdir_obj[file] = "FILE"

            if depth < maxdepth:
                for subdir in subdirs:
                    subpath = os.path.join(path, subdir)

                    result = get_directory_structure_to_some_depth(subpath, start_time, depth+1, maxdepth)

                    if result is not None:
                        # Everything is normal
                        subdir_obj[subdir] = result
                    else:
                        # We've timed out and need to finish request ASAP
                        break
            
            if depth == 0:
                return {path: subdir_obj}
            else:
                return subdir_obj
                
        # os.walk should only exit immediately if we don't have permission to read the given directory
        return "PERMISSION DENIED"
    except Exception as e:
        print(e)
        return {}

@router.get("")
async def endpoints():
    return {"http": http_endpoints, "ws": ws_endpoints}