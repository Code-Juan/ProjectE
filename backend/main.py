import os
from fastapi import FastAPI, WebSocket
import json
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read variables from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Store connected clients
connected_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    
    try:
        # Fetch old messages from Supabase
        previous_messages = supabase.table("messages").select("message").execute()
        
        # Send previous messages to the new client
        for record in previous_messages.data:
            await websocket.send_text(json.dumps({"previous_message": record["message"]}))

        while True:
            # Receive message from WebSocket
            data = await websocket.receive_text()
            print(f"Received: {data}")

            # Store message in Supabase asynchronously
            async def save_message():
                response = supabase.table("messages").insert({"message": data}).execute()
                print(f"Stored in Supabase: {response}")

            await save_message() # Run asynchronously

            # Send response to all clients
            for client in connected_clients:
                await client.send_text(json.dumps({"message": f"Processed: {data}"}))

    except Exception as e:
        print(f"Connection closed: {e}")
        connected_clients.remove(websocket)
