import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import redis.asyncio as redis
import uuid
import json

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(REDIS_URL, decode_responses=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

EMAIL_DOMAIN = "tempmail.render"  # temporary domain name

@app.get("/generate-email")
async def generate_email():
    email_id = str(uuid.uuid4())[:8]
    email = f"{email_id}@{EMAIL_DOMAIN}"
    await r.setex(email, 3600, "[]")
    return {"email": email}

@app.get("/messages/{email}")
async def get_messages(email: str):
    data = await r.get(email)
    return {"messages": json.loads(data) if data else []}

@app.post("/receive")
async def receive_email(request: Request):
    data = await request.json()
    to_email = data.get("to")
    message = {
        "from": data.get("from"),
        "subject": data.get("subject"),
        "body": data.get("body")
    }
    existing = await r.get(to_email)
    messages = json.loads(existing) if existing else []
    messages.append(message)
    await r.set(to_email, json.dumps(messages))
    return JSONResponse({"status": "received"})
