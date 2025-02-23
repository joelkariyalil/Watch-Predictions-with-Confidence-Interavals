import openai
import redis
import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load API Key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing!")

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

basePrompt = '''

This is the requirement Pls analyse the text, and pls create a tokenized parameters only in this format:
    Listing code: K2A6N0
    Brand: Rolex
    Model: GMT-Master II
    Reference number: 16713
    Movement: Automatic
    Case material: Gold/Steel
    Bracelet material: Gold/Steel
    Year of production: 1988
    Condition:  
    Scope of delivery:  
    Gender: Men's watch/Unisex
    Location: United States of America: Florida: Ft Lauderdale
    Price: $10:500
    Availability: Item is in stock
    Movement: Automatic
    Caliber/movement: 3185
    Base caliber: Rolex 3135
    Power reserve: 48 h
    Number of jewels: 31
    Case material: Gold/Steel
    Case diameter:  
    Water resistance: 10 ATM
    Bezel material: Yellow gold
    Crystal: Sapphire crystal
    Dial: Black
    Dial numerals: No numerals
    Bracelet material: Gold/Steel
    Bracelet color: Gold/Steel
    Clasp: Fold clasp
    Clasp material: Steel

    Return the above list in the format of a json object!
    and if any of the values are not available, pls return "N/A" in the json object!

'''
@app.post("/chat")
async def chat(request: ChatRequest):

    prompt = basePrompt+request.prompt
    
    prompt = request.prompt.strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        # Call OpenAI API asynchronously
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )

        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        answer = data["choices"][0]["message"]["content"]

        return {"response": answer, "cached": False}

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="OpenAI API error")
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Failed to connect to OpenAI API")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
