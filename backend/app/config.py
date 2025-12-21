"""
Application Configuration
Load environment variables securely using pydantic-settings
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "jobs_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    
    # API Configuration
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    
    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),  # Check both backend folder and project root
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property
    def database_url(self) -> str:
        """Construct database URL from components with proper encoding."""
        from urllib.parse import quote_plus
        # URL encode password to handle special characters like @, !, #, etc.
        encoded_password = quote_plus(self.POSTGRES_PASSWORD)
        return (
            f"postgresql://{self.POSTGRES_USER}:{encoded_password}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
