#!/usr/bin/env python

import asyncio
import json
import websockets
import uuid


connected = set()


async def consumer(websocket, message):
    global connected

    try:
        if ('messageId' in json.loads(message).keys()):

            await asyncio.wait([socket.send(json.dumps({'relatesTo': json.loads(message)['messageId'], 'data': message, 'messageId': str(uuid.uuid4())})) for socket in connected])
            print(message)
    except Exception as e:
        print(e)


async def consumer_handler(websocket):
    while True:
        message = await websocket.recv()
        await consumer(websocket, message)


async def handler(websocket, path):
    global connected
    connected.add(websocket)
    try:
        print("New websocket connected")
        await asyncio.wait([ws.send("Hello!") for ws in connected])

        consumer_task = asyncio.ensure_future(
            consumer_handler(websocket))

        done, pending = await asyncio.wait(
            [consumer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

    finally:
        print("closing")
        connected.remove(websocket)


start_server = websockets.serve(handler, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
