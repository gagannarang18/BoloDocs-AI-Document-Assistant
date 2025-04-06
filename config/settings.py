from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # AstraDB Configuration
    ASTRA_DB_APPLICATION_TOKEN: str
    ASTRA_DB_API_ENDPOINT: str
    
    # Gemini Configuration
    GEMINI_API_KEY: str
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-west-2"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()