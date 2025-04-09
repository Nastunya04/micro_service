from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Record(BaseModel):
    original_text: str
    translated_text: str
    target_language: str
    detected_language: str

db_storage: List[Record] = []

@app.get("/")
async def index():
    return "Database Service: Store translation records."

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/write")
async def write(record: Record):
    db_storage.append(record)
    return {"message": "Record saved.", "record": record}

@app.get("/read")
async def read():
    return {"records": db_storage}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5003, debug=True)