from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json
import requests
import os
import time  

app = FastAPI()

API_KEY = os.getenv("ALAN_API_KEY")
headers = {"Authorization": f"Bearer {API_KEY}"}

def generate_response():
    """ Antwort von Alan API wirklich als Stream ausgeben """
    url = "https://app.alan.de/api/v1/llm/generate_stream"
    payload = json.dumps({
        "messages": [
            {"content": "Was sind die neuen Features der Baloise-Berufsunfähigkeitsversicherung?", "role": "user"}
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800,
        "model": "comma-soft/comma-llm-l-v3"
    })

    response = requests.post(url, headers=headers, data=payload, stream=True)

    for chunk in response.iter_content(chunk_size=64): 
        if chunk:
            yield chunk.decode()  
            time.sleep(0.1) 

@app.get("/stream")
async def stream_response():
    return StreamingResponse(generate_response(), media_type="text/plain")
