from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    
    This class defines all configuration parameters needed for the application
    to run, including database URLs, JWT settings, and other environment-specific
    configurations.
    
    Attributes:
        mysql_url (str): Database connection URL (supports SQLite and MySQL)
        jwt_secret (str): Secret key for JWT token signing and verification
        jwt_alg (str): Algorithm used for JWT token encoding/decoding
        access_token_expire_minutes (int): JWT token expiration time in minutes
    """
    
    mysql_url: str = Field(
        ..., 
        env="MYSQL_URL",
        description="Database connection URL"
    )
    jwt_secret: str = Field(
        ..., 
        env="JWT_SECRET",
        description="Secret key for JWT token signing"
    )
    jwt_alg: str = Field(
        "HS256", 
        env="JWT_ALG",
        description="Algorithm for JWT token encoding"
    )
    access_token_expire_minutes: int = Field(
        60, 
        env="ACCESS_TOKEN_EXPIRE_MINUTES",
        description="JWT token expiration time in minutes"
    )

    class Config:
        """Pydantic configuration for settings loading."""
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()