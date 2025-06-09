
from fastapi import FastAPI, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import httpx
from googletrans import Translator
import asyncio


app = FastAPI()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
translator = Translator(service_urls=[
      'translate.googleapis.com'
    ])

@app.get("/")
async def root():
    return {"message": "World World"}

async def get_translation_result(message):
    # Await the translate method to get the actual translation result
    result = await translator.translate(message)
    return result.text

# Add rate limit exception handler
@app.exception_handler(RateLimitExceeded)
#async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
#    return JSONResponse(
#        status_code=429,
#        content={"detail": "Rate limit exceeded. Try again later."}
#    )

# Define request model
class TranslationRequest(BaseModel):
    message: str

# Define translation endpoint with rate limiting
@app.post("/translate")
#@limiter.limit("5/minute")
async def translate(request: TranslationRequest):
    async with httpx.AsyncClient() as client:
        result = translator.translate(request.message)
        translation = await get_translation_result(request.message)
        #response = await client.post(
        #    "https://libretranslate.de/translate",
        #    json={
        #        "q": request.message,
        #        "source": "auto",
        #        "target": "en",
        #        "format": "text", 
        #        "alternatives": 3,
		#        "api_key": ""
        #    }
        #)
        #translated_text = response.json()["translatedText"]
        translated_text = translation
    return {"translatedText": translated_text}
