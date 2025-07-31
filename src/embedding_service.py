"""
Embedding Service Module

This module handles all embedding generation logic using Google's Gemini model.

MIT License
Copyright (c) 2025 Arman Maurya
"""

from typing import List
import numpy as np
from google import genai
from google.genai import types
import os


class EmbeddingService:
    """Service class for generating embeddings using Google's Gemini model."""
    
    def __init__(self, api_key: str):
        """Initialize the embedding service with Google AI API key."""
        if not api_key:
            raise ValueError("API key is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-embedding-001"
        self.default_dimensions = 768
    
    def generate_single_embedding(self, text: str, normalize: bool = True, dimensions: int = None) -> dict:
        """
        Generate a single embedding for the given text.
        
        Args:
            text (str): The text to generate embedding for
            normalize (bool): Whether to normalize the embedding vector
            dimensions (int): Output dimensions (default: 768)
            
        Returns:
            dict: Contains the embedding vector and metadata
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        dimensions = dimensions or self.default_dimensions
        
        try:
            # Generate embedding using Gemini model
            result = self.client.models.embed_content(
                model=self.model,
                contents=text,
                config=types.EmbedContentConfig(output_dimensionality=dimensions)
            )
            
            # Extract embedding values
            embeddings = result.embeddings[0].values
            
            # Normalize if requested
            if normalize:
                embedding_values_np = np.array(embeddings)
                embeddings = (embedding_values_np / np.linalg.norm(embedding_values_np)).tolist()
            
            return {
                "text": text,
                "embedding": embeddings,
                "dimension": len(embeddings),
                "normalized": normalize,
                "model": self.model
            }
        
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")
