#!/usr/bin/env python

import json
import websockets
import uuid
import asyncio
import classes.MessageValidator as mv
from collections import namedtuple


class WSServer:

    connected = set()

    async def consumer(self, websocket, message):
        try:
            msg = json.loads(message)
            mv.validate_message(msg)
            msg = mv.parse_message(message)

            if msg.get('type') == "REGULAR":
                await self.send_all(json.dumps(msg))
            else:
                await self.send_all(
                    json.dumps(
                        {
                            'relatesTo': msg.get('id'),
                            'data': msg,
                            'id': str(uuid.uuid4()),
                            'type': 'DEBUG'
                        }))
            print(message)

        except Exception as e:
            print("message format not supported:" + str(e));
            print("message :")
            print(message)

    async def send_all(self, message):
        await asyncio.wait([socket.send(message) for socket in self.connected])

    async def send_all_except(self, no_receivers, message):
        await asyncio.wait([socket.send(message) for socket in self.connected - no_receivers])

    async def consumer_handler(self, websocket):
        while True:
            message = await websocket.recv()
            await self.consumer(websocket, message)

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        print(path)
        try:
            print("New websocket connected")
            await asyncio.wait([websocket.send(
                json.dumps({'messageId': str(uuid.uuid4()),
                            'message': 'Hello Client'})
            )])

            consumer_task = asyncio.ensure_future(
                self.consumer_handler(websocket))

            done, pending = await asyncio.wait(
                [consumer_task],
                return_when=asyncio.FIRST_COMPLETED,
            )

            for task in pending:
                task.cancel()

        finally:
            print("closing")
            self.connected.remove(websocket)

    def start(self):
        start_server = websockets.serve(self.handler, self.name, self.port)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def __init__(self, name, port):
        self.name = name
        self.port = port
