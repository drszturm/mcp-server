from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # DeepSeek API Configuration
    DEEPSEEK_API_KEY: str
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    # MCP Server Configuration
    MCP_SERVER_NAME: str = "deepseek-mcp-server"
    MCP_SERVER_VERSION: str = "1.0.0"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    REDIS_URL: Optional[str] = None

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
