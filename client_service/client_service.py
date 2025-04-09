import os
import sys
import requests
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

FIXED_TOKEN = os.getenv("CLIENT_SERVICE_TOKEN")
if not FIXED_TOKEN:
    sys.exit("Error: CLIENT_SERVICE_TOKEN environment variable is not set. Please set it before running the service.")

app = FastAPI()

class TranslateRequest(BaseModel):
    text: str
    target_language: str

@app.get("/")
async def index():
    return "Client Service: Public API for text translation. Use your token to access."

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/some-protected-route")
async def protected_route(authorization: str = Header(None)):
    if authorization != f"Bearer {FIXED_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "You are authorized!"}

@app.post("/translate")
async def translate(request_data: TranslateRequest, authorization: str = Header(None)):
    if authorization != f"Bearer {FIXED_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    BUSINESS_SERVICE_URL = "http://business_service:5002/process"
    try:
        business_response = requests.post(BUSINESS_SERVICE_URL, json=request_data.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Business Service: {str(e)}")

    if business_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Business Service processing failed.")

    business_result = business_response.json()

    db_payload = {
        "original_text": request_data.text,
        "translated_text": business_result.get("translated_text", ""),
        "target_language": request_data.target_language,
        "detected_language": business_result.get("detected_language_of_request", "unknown")
    }

    DATABASE_WRITE_URL = "http://database_service:5003/write"
    try:
        db_response = requests.post(DATABASE_WRITE_URL, json=db_payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Database Service: {str(e)}")

    if db_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to save record in the database.")

    return business_result

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, debug=True)
