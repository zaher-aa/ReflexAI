from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Text Analysis Tool"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: set = {".txt"}
    
    DELETE_AFTER_ANALYSIS: bool = True
    
    OLLAMA_MODEL: str = "llama3.1"
    
    class Config:
        env_file = ".env"

settings = Settings()