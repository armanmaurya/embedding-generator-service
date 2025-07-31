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
    
    def generate_batch_embeddings(self, texts: List[str], normalize: bool = True, dimensions: int = None) -> List[dict]:
        """
        Generate embeddings for multiple texts in a single request.
        
        Args:
            texts (List[str]): List of texts to generate embeddings for
            normalize (bool): Whether to normalize the embedding vectors
            dimensions (int): Output dimensions (default: 768)
            
        Returns:
            List[dict]: List of embedding results with metadata
        """
        if not texts or len(texts) == 0:
            raise ValueError("Texts list cannot be empty")
        
        # Validate all texts are non-empty
        for i, text in enumerate(texts):
            if not text or not text.strip():
                raise ValueError(f"Text at index {i} cannot be empty")
        
        dimensions = dimensions or self.default_dimensions
        
        try:
            # Generate embeddings for all texts at once
            result = self.client.models.embed_content(
                model=self.model,
                contents=texts,
                config=types.EmbedContentConfig(output_dimensionality=dimensions)
            )
            
            embeddings_list = []
            for i, text in enumerate(texts):
                embeddings = result.embeddings[i].values
                
                # Normalize if requested
                if normalize:
                    embedding_values_np = np.array(embeddings)
                    embeddings = (embedding_values_np / np.linalg.norm(embedding_values_np)).tolist()
                
                embeddings_list.append({
                    "text": text,
                    "embedding": embeddings,
                    "dimension": len(embeddings),
                    "normalized": normalize,
                    "model": self.model
                })
            
            return embeddings_list
        
        except Exception as e:
            raise Exception(f"Failed to generate batch embeddings: {str(e)}")
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1 (List[float]): First embedding vector
            embedding2 (List[float]): Second embedding vector
            
        Returns:
            float: Cosine similarity score between -1 and 1
        """
        if len(embedding1) != len(embedding2):
            raise ValueError("Embeddings must have the same dimension")
        
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
