from fastapi import FastAPI, Request, HTTPException
import requests
import socket
import uuid

app = FastAPI()

CHATGPT_SERVICE_URL = "http://chatgpt_service:5001/chat"

@app.get("/")
def ping():
    return {"message": "Hello from FastAPI!"}

def createSessionID():
    return str(uuid.uuid4())

sesssionID = createSessionID()

@app.get("/query")
async def query(message: str, request: Request):
    """Calls the ChatGPT service and returns the response."""
    
    response = await ask_chatgpt(, message, request)
    
    return {"message": str(message) + " Response: " + response["response"]}


async def ask_chatgpt(sessionID, prompt: str, request: Request):
    """Forwards request to the ChatGPT service container, but only allows internal Docker services."""

    response = requests.post(CHATGPT_SERVICE_URL, json={"sessionID": sessionID, "prompt": prompt})

    if response.status_code == 200:
        return response.json()

    return {"Error": "Failed to connect to ChatGPT service"}