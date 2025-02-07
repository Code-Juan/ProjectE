from fastapi import FastAPI, WebSocket
import json

app = FastAPI()

# Store connected clients
connected_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    
    try:
        while True:
            # Receive data from client
            data = await websocket.receive_text()
            print(f"Received: {data}")
            
            # Send response to all connected clients
            for client in connected_clients:
                await client.send_text(json.dumps({"message": f"Processed: {data}"}))
    
    except Exception as e:
        print(f"Connection closed: {e}")
        connected_clients.remove(websocket)
