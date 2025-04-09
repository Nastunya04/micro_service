from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator

app = FastAPI()

class ProcessPayload(BaseModel):
    text: str
    target_language: str

@app.get("/")
async def index():
    return "Business Service: Preprocess and translate text in one service."

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/process")
async def process_text(payload: ProcessPayload):
    raw_text = payload.text
    normalized_text = raw_text.strip().lower()

    try:
        detected_language = detect(raw_text)
    except LangDetectException:
        detected_language = "unknown"

    target_language = payload.target_language
    try:
        translator = GoogleTranslator(source="auto", target=target_language)
        translated_text = translator.translate(normalized_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

    result = {
        "detected_language_of_request": detected_language,
        "target_language": target_language,
        "translated_text": translated_text
    }
    return result

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002, debug=True)