import json
from typing import Dict, List, Tuple
from global_variables import GLOBAL_VARIABLES
from pydantic_models.loop import Loop
from pydantic_models.tag_group import Tag_Group
from fastapi import WebSocket
from asyncio import create_task, gather, sleep

from pydantic_models.ui_client import UI_Client

from asyncua import Client

# class OPC_Client(Client):
class OPC_Client():
    url = GLOBAL_VARIABLES.opc_url

    idx = GLOBAL_VARIABLES.opc_idx

    clients: Dict[str, UI_Client] = {}

    validated_tags = set()

    tags_to_read = {}

    native_client: Client

    def __init__(self):
        # super().__init__(self.url, 4)
        self.native_client = Client(self.url)

    async def test_connection(self):
        try:
            result = await self.native_client.connect()
            print("OPC SUCCESS", result)
            return result
        except Exception as e:
            print("OPC ERROR:", e)
            return e
    
    def register_new_client(self, client_id, ws):
        self.clients[client_id] = UI_Client(ws=ws, loops=[])
    
    async def read_tag_list(self, tags):
        output = {}
        errors = {}
        tasks = []

        for tag in tags:
            task = create_task(self.read_tag(tag))
            tasks.append(task)
        
        results = await gather(*tasks)
        for tag, value in results:
            if isinstance(value, Exception):
                errors[tag] = str(value)
            else:
                output[tag] = value
        
        return output, errors
    
    async def read_tag(self, tag: str):
        try:
            node_name = self.idx + tag
            node_obj = self.native_client.get_node(node_name)
            return tag, await node_obj.read_value()
        except Exception as e:
            return tag, e
    
    async def validate_tags(self, tags) -> Tuple[List[str], List[str]]:
        prevalidated_list = []
        unvalidated_list = []

        for tag in tags:
            if tag in self.validated_tags:
                prevalidated_list.append(tag)
            else:
                unvalidated_list.append(tag)

        output, errors = await self.read_tag_list(unvalidated_list)
        invalid_tags = list(errors.keys())
        valid_tags = list(output.keys()) + prevalidated_list

        for tag in output.keys():
            self.validated_tags.add(tag)
            
        return invalid_tags, valid_tags
    
    async def update_reads(self, client_id, tag_groups: List[Tag_Group]):
        total_invalid_tags = []

        ui_client = self.clients[client_id]

        if not ui_client:
            return "unregistered client"
        
        self.stop_one_client_loops(client_id)

        for group in tag_groups:

            invalid_tags, valid_tags = await self.validate_tags(group.Tags)

            total_invalid_tags += invalid_tags

            task = create_task(self.run_tag_reading_loop(group.Interval_ms, valid_tags, ui_client.ws))

            self.clients[client_id].loops.append(Loop(freq=group.Interval_ms, task=task, tags=valid_tags))
        
        return total_invalid_tags

    async def run_tag_reading_loop(self, freq: int, tags: List[str], client_ws: WebSocket):
        i = 0
        while True:
            output, errors = await self.read_tag_list(tags)

            await client_ws.send_json(output)

            if errors != {}:
                await client_ws.send_json({"Type": "RW_error", "Read Request Failed": json.dumps(errors)})

            i += 1
            await sleep(freq / 1000)
    
    def stop_one_client_loops(self, client_id):
        client = self.clients[client_id]

        for loop in client.loops:
            loop.task.cancel()
        
        client.loops = []
    
    def cleanup_one_client(self, client_id):
        print("Cleaning up", client_id)

        self.stop_one_client_loops(client_id)

        del self.clients[client_id]
    
    def cleanup_all_clients(self):
        for client_id in self.clients:
            self.cleanup_one_client(client_id)
