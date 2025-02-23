import redis
import requests
import numpy as np
import pandas as pd
from fastapi import FastAPI
from sklearn.linear_model import LinearRegression

# Connect to Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# Vector Database API endpoint
VECTOR_DB_HOST = "http://vector_db:6333"

app = FastAPI()

# Dummy model (Replace with real model logic)
model = LinearRegression()

@app.post("/predict")
async def predict(features: list):
    """Predicts watch price based on input features."""
    
    # Check Redis cache first
    cache_key = str(features)
    cached_prediction = redis_client.get(cache_key)
    if cached_prediction:
        return {"prediction": float(cached_prediction), "cached": True}

    # Placeholder model logic
    features_array = np.array(features).reshape(1, -1)
    prediction = model.predict(features_array)[0]

    # Cache result in Redis
    redis_client.setex(cache_key, 3600, prediction)

    return {"prediction": float(prediction), "cached": False}
