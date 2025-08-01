"""
Data Models for the Embedding API

This module contains all Pydantic models used for request/response validation.

MIT License
Copyright (c) 2025 Arman Maurya
"""

from typing import List, Optional
from pydantic import BaseModel, Field

class ArticleEmbeddingRequest(BaseModel):
    """Request model for article embedding generation."""
    article_id: str = Field(..., description="Unique identifier for the article")
    text: str = Field(..., description="The text content of the article", min_length=1)
    normalize: bool = Field(True, description="Whether to normalize the embedding vector")
    dimensions: int = Field(768, description="Output embedding dimensions", ge=128, le=3072)

class CloudTasksPayload(BaseModel):
    """Request model for Google Cloud Tasks payload."""
    task_type: str = Field(..., description="Type of task")
    timestamp: str = Field(..., description="Timestamp of task creation")
    article_embedding_request: ArticleEmbeddingRequest = Field(..., description="Article embedding request data")

class ArticleEmbeddingResponse(BaseModel):
    """Response model for article embedding generation."""
    status: str = Field(..., description="Status of the embedding generation")
    article_id: str = Field(..., description="Unique identifier for the article")

class EmbeddingRequest(BaseModel):
    """Request model for single embedding generation."""
    text: str = Field(..., description="The text to generate embedding for", min_length=1)
    normalize: bool = Field(True, description="Whether to normalize the embedding vector")
    dimensions: int = Field(768, description="Output embedding dimensions", ge=128, le=3072)


class EmbeddingResponse(BaseModel):
    """Response model for single embedding."""
    text: str = Field(..., description="The text for which embedding was generated")
    embedding: List[float] = Field(..., description="The embedding vector")
    dimension: int = Field(..., description="Dimension of the embedding")
    normalized: bool = Field(..., description="Whether the embedding was normalized")
    model: str = Field(..., description="The model used to generate the embedding")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service status")
    model: str = Field(..., description="Embedding model being used")
    version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Response model for errors."""
    detail: str = Field(..., description="Error message")
    error_type: str = Field(..., description="Type of error")
