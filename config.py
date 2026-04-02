# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Remove DATABASE_URL
    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: str = "gemini-3-flash-preview" # Default model, can be changed
    STUDENT_DATA_FILE: str = "student_data.json" # Path to the JSON file

    class Config:
        env_file = ".env"

settings = Settings()