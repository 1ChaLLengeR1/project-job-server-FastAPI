import json
import asyncio
from fastapi import WebSocket

active_connections = {}


async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    active_connections[client_id] = websocket

    try:
        while True:
            await websocket.receive_text()
    except:
        pass
    finally:
        del active_connections[client_id]


def send_progress(client_id: str, progress: int, message: str):
    if client_id in active_connections:
        try:
            asyncio.run(active_connections[client_id].send_text(json.dumps({"progress": progress, "message": message})))
        except Exception as e:
            print(f"❌ Błąd wysyłania do klienta {client_id}: {e}")
