
from fastapi import FastAPI, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import httpx
from googletrans import Translator
import asyncio


app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
translator = Translator(service_urls=[
      'translate.googleapis.com'
    ])

@app.get("/")
async def root():
    return {"message": "World World"}

async def get_translation_result(text_message):
    result = await translator.translate(text_message)
    return result.text

# Add rate limit exception handler
@app.exception_handler(RateLimitExceeded)
#async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
#    return JSONResponse(
#        status_code=429,
#        content={"detail": "Rate limit exceeded. Try again later."}
#    )

class TranslationRequest(BaseModel):
    message: str

# Define translation endpoint with rate limiting
@app.post("/translate")
#@limiter.limit("5/minute")
async def translate(request: TranslationRequest):
    async with httpx.AsyncClient() as client:
        #result = translator.translate(request.message)
        text_result = await get_translation_result(request.message)
        translated_text = text_result
    return {"translatedText": translated_text}
