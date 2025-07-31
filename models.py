"""
Data Models for the Embedding API

This module contains all Pydantic models used for request/response validation.

MIT License
Copyright (c) 2025 Arman Maurya
"""

from typing import List
from pydantic import BaseModel, Field


class EmbeddingRequest(BaseModel):
    """Request model for single embedding generation."""
    text: str = Field(..., description="The text to generate embedding for", min_length=1)
    normalize: bool = Field(True, description="Whether to normalize the embedding vector")
    dimensions: int = Field(768, description="Output embedding dimensions", ge=128, le=3072)


class EmbeddingResponse(BaseModel):
    """Response model for single embedding."""
    text: str = Field(..., description="The original input text")
    embedding: List[float] = Field(..., description="The embedding vector")
    dimension: int = Field(..., description="The dimension of the embedding")
    normalized: bool = Field(..., description="Whether the embedding is normalized")
    model: str = Field(..., description="The model used to generate the embedding")


class BatchEmbeddingRequest(BaseModel):
    """Request model for batch embedding generation."""
    texts: List[str] = Field(..., description="List of texts to generate embeddings for", min_items=1, max_items=100)
    normalize: bool = Field(True, description="Whether to normalize the embedding vectors")
    dimensions: int = Field(768, description="Output embedding dimensions", ge=128, le=3072)


class BatchEmbeddingResponse(BaseModel):
    """Response model for batch embeddings."""
    embeddings: List[EmbeddingResponse] = Field(..., description="List of embedding results")
    total_count: int = Field(..., description="Total number of embeddings generated")


class SimilarityRequest(BaseModel):
    """Request model for similarity calculation."""
    text1: str = Field(..., description="First text for comparison", min_length=1)
    text2: str = Field(..., description="Second text for comparison", min_length=1)
    normalize: bool = Field(True, description="Whether to normalize embeddings before comparison")


class SimilarityResponse(BaseModel):
    """Response model for similarity calculation."""
    text1: str = Field(..., description="First input text")
    text2: str = Field(..., description="Second input text")
    similarity: float = Field(..., description="Cosine similarity score between -1 and 1")
    embedding1: List[float] = Field(..., description="Embedding of the first text")
    embedding2: List[float] = Field(..., description="Embedding of the second text")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service status")
    model: str = Field(..., description="Embedding model being used")
    version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Response model for errors."""
    detail: str = Field(..., description="Error message")
    error_type: str = Field(..., description="Type of error")
