import os
from dotenv import load_dotenv

# .env file load karo
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Construction RFP Analyzer"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

settings = Settings()