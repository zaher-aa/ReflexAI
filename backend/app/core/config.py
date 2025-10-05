from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Text Analysis Tool"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: set = {".txt"}
    
    DELETE_AFTER_ANALYSIS: bool = True
    CLEANUP_INTERVAL_SECONDS: int = 1800
    MAX_FILE_AGE_SECONDS: int = 3600
    
    OLLAMA_MODEL: str = "llama3.2:1b"
    OLLAMA_HOST: str = "http://localhost:11434"
    
    class Config:
        env_file = ".env"

settings = Settings()