import asyncio
import os
import websockets

PORT = int(os.environ.get("PORT", 8080))
clients = set()

async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            for c in clients:
                if c != websocket:
                    await c.send(message)
    finally:
        clients.remove(websocket)

async def main():
    print("Server running")
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()

asyncio.run(main())