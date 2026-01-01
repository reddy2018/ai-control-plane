from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "AI Control Plane"
    version: str = "0.1.0"
    environment: str = "dev"
    
settings = Settings()