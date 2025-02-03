import asyncio
import websockets  # note the plural 's'
import json

# Set of connected clients
clients = set()

async def handler(websocket, path):
    # Add new client connection
    clients.add(websocket)
    print("New client connected")
    try:
        async for message in websocket:
            # Broadcast the received annotation to all other clients
            print("Received message:", message)
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except Exception as e:
        print("Exception:", e)
    finally:
        clients.remove(websocket)
        print("Client disconnected.")

async def main():
    async with websockets.serve(handler, "localhost", 6789):
        print("WebSocket server started at ws://localhost:6789")
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
