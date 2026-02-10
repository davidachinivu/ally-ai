import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Model preferences
    GEMINI_MODEL = "gemini-flash-latest" # Confirmed available in user's debug list
    
    # App Settings
    APP_NAME = "AllyAI"
    VERSION = "2.1.0 (Gemini Edition)"
