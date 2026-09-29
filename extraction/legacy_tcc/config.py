import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_VISION_API_KEY = os.getenv("GOOGLE_VISION_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_VISION_API_KEY or not GEMINI_API_KEY:
    raise ValueError("Chaves de API não encontradas. Verifique seu arquivo .env")