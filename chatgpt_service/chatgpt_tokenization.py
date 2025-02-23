import openai
import redis
import os
from fastapi import FastAPI

# Load API Key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Connect to Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

app = FastAPI()

@app.post("/chat")
async def chat(prompt: str):
    """Handles ChatGPT requests and caches responses in Redis."""
    
    # Check if response is cached
    cached_response = redis_client.get(prompt)
    if cached_response:
        return {"response": cached_response, "cached": True}

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract response text
    answer = response["choices"][0]["message"]["content"]

    # Cache response in Redis for 1 hour
    redis_client.setex(prompt, 3600, answer)

    return {"response": answer, "cached": False}
