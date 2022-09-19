from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from opcua.opc_client import OPC_Client
from global_variables import GLOBAL_VARIABLES
from pydantic_models.UI_Request_Init import UI_Request_Init
from pydantic_models.UI_Request_RW import UI_Request_RW

opc_client = OPC_Client()

PREFIX = "/uiredesign"

router = APIRouter(
    prefix=PREFIX
)

http_endpoints = []
ws_endpoints = []

@router.on_event("startup")
def startup():
    print("Application is booting up")

@router.on_event("shutdown")
def cleanup():
    # Ensuring all loops are shutdown
    opc_client.cleanup_all_clients()

# Entire logic for communicating with UI will be here
ws_endpoints.append("/ws")
@router.websocket("/ws")
async def ui_ws(websocket: WebSocket):
    await websocket.accept()

    client_id = websocket.client.host + ":" + str(websocket.client.port)

    # We first wait for init message and act accordingly
    try:
        opc_client.register_new_client(client_id, websocket)

        obj = await websocket.receive_json()
        init = UI_Request_Init.parse_obj(obj)

        status = await opc_client.test_connection()

        if isinstance(status, Exception):
            raise status

        invalid_tags, valid_tags = await opc_client.validate_tags(init.Tag)

        # If OPC response was bad, let client know and break connection
        if len(invalid_tags) != 0:
            print("Init contained invalid tags:", invalid_tags)
            await websocket.send_json({"Invalid Tags": invalid_tags})
        else:
            # print(client_id, "initted successfully")
            await websocket.send_json({"Success": True})

    except Exception as e:
        # Let UI know they gave a wrongly formatted object and break connection
        print("ERROR!", client_id, e)
        
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.send_json({"Error": str(e)})

    # We now wait for any RW messages
    try:
        while True:
            obj = await websocket.receive_json()
            rw = UI_Request_RW.parse_obj(obj)
            # print("RW parsed successfully")

            # Update reading loop and perform writes
            result = await opc_client.update_reads(client_id, rw.Request.Read)

            if result == []:
                print(client_id, "is reading successfully")
            else:
                print(client_id, "contained erroneous tags or has error:", result)

                if isinstance(result, list):
                    await websocket.send_json({"Type": "INIT/Setup_errror", "Tags": result})
                else:
                    await websocket.send_json({"Type": "RW_error", "Read Request Failed": str(result)})

            # No need to break out of loop, we simply listen for next message until client shuts down
    
    # If any errors occur, stop reading loops and return error
    except WebSocketDisconnect as e:
        print(client_id, "disconnected with code", e.code)
    except Exception as e:
        print("ERROR!", client_id, e)
        
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.send_json({"Error": str(e)})
    finally:
        opc_client.cleanup_one_client(client_id)

@router.get("")
async def endpoints():
    return {"http": http_endpoints, "ws": ws_endpoints}
