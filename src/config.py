"""
Configuration Management

This module handles loading and validation of configuration from environment variables.

MIT License
Copyright (c) 2025 Arman Maurya
"""

import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration class for the embedding API."""
    
    def __init__(self):
        """Initialize configuration by loading environment variables."""
        # Load environment variables from .env file
        load_dotenv()
        
        # API Configuration
        self.google_ai_api_key = self._get_required_env("GOOGLE_AI_API_KEY")
        
        # App Configuration
        self.app_name = os.getenv("APP_NAME", "Embedding Generator API")
        self.app_description = os.getenv("APP_DESCRIPTION", "Generate 768-dimensional embeddings using Google's Gemini model")
        self.app_version = os.getenv("APP_VERSION", "1.0.0")
        
        # Server Configuration
        self.host = os.getenv("HOST", "127.0.0.1")
        self.port = int(os.getenv("PORT", "8000"))
        self.reload = os.getenv("RELOAD", "true").lower() == "true"
        
        # Embedding Configuration
        self.default_model = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
        self.default_dimensions = int(os.getenv("DEFAULT_DIMENSIONS", "768"))
        
        # Rate Limiting (for future implementation)
        self.rate_limit_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", "100"))

        self.save_embedding_api_endpoint = os.getenv("SAVE_EMBEDDING_API_ENDPOINT")
        
    def _get_required_env(self, key: str) -> str:
        """Get required environment variable or raise error if not found."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value
    
    def validate(self) -> bool:
        """Validate configuration settings."""
        try:
            # Validate API key exists
            if not self.google_ai_api_key:
                raise ValueError("Google AI API key is required")
            
            # Validate dimensions
            if not 128 <= self.default_dimensions <= 3072:
                raise ValueError("Default dimensions must be between 128 and 3072")
            
            # Validate port
            if not 1 <= self.port <= 65535:
                raise ValueError("Port must be between 1 and 65535")
            
            return True
            
        except Exception as e:
            print(f"Configuration validation failed: {e}")
            return False
    
    def get_fastapi_config(self) -> dict:
        """Get configuration dictionary for FastAPI app initialization."""
        return {
            "title": self.app_name,
            "description": self.app_description,
            "version": self.app_version,
        }
    
    def get_uvicorn_config(self) -> dict:
        """Get configuration dictionary for Uvicorn server."""
        return {
            "host": self.host,
            "port": self.port,
            "reload": self.reload,
        }


# Global config instance
config = Config()
