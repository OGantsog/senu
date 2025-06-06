
from fastapi import FastAPI, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import httpx

app = FastAPI()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

@app.get("/")
async def root():
    return {"message": "World World"}

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
        response = await client.post(
            "https://libretranslate.de/translate",
            json={
                "q": request.message,
                "source": "auto",
                "target": "en",
                "format": "text", 
                "alternatives": 3,
		        "api_key": ""
            }
        )
        translated_text = response.json()["translatedText"]
    return {"translatedText": translated_text}
