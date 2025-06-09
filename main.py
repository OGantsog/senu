# prompt: Can you write API using this googletrans that translates any text message into english?

from fastapi import FastAPI
from googletrans import Translator
import asyncio

# Initialize the FastAPI application
app = FastAPI()

# Initialize the translator
# Ensure googletrans is installed by running !pip install googletrans if needed
translator = Translator(service_urls=[
      'translate.googleapis.com'
    ])

# Define an asynchronous function to get translation
async def get_translation_result(message: str):
    """
    Translates the given message to English.

    Args:
        message (str): The text message to translate.

    Returns:
        str: The translated text in English.
    """
    # Translate the message to English
    # We specify the destination language as 'en' (English)
    result = await asyncio.to_thread(translator.translate, message, dest='en')
    return result.text

# Define an API endpoint for translation
@app.get("/translate")
async def translate_text(text: str):
    """
    API endpoint to translate a given text message to English.

    Args:
        text (str): The text message to translate.

    Returns:
        dict: A dictionary containing the original text and the translated text.
    """
    translated_text = await get_translation_result(text)
    return {"original_text": text, "translated_text": translated_text}
