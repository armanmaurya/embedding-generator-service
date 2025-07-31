"""
FastAPI Embedding Generator API

Main application file that defines API routes and handles HTTP requests.

MIT License
Copyright (c) 2025 Arman Maurya
"""

from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# Import our custom modules
from .config import config
from .embedding_service import EmbeddingService
from .models import (
    EmbeddingRequest, EmbeddingResponse,
    BatchEmbeddingRequest, BatchEmbeddingResponse,
    SimilarityRequest, SimilarityResponse,
    HealthResponse, ErrorResponse
)

# Validate configuration
if not config.validate():
    raise RuntimeError("Invalid configuration. Please check your environment variables.")

# Initialize FastAPI app with config
app = FastAPI(**config.get_fastapi_config())

# Initialize embedding service
embedding_service = EmbeddingService(api_key=config.google_ai_api_key)


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}", "error_type": "InternalServerError"}
    )


@app.get("/", response_model=dict)
def read_root():
    """Root endpoint with API information."""
    return {
        "message": config.app_name,
        "version": config.app_version,
        "endpoints": {
            "/embed": "Generate single embedding",
            "/embed/batch": "Generate multiple embeddings",
            "/similarity": "Calculate similarity between two texts",
            "/health": "Health check",
            "/docs": "API documentation"
        },
        "model": config.default_model,
        "default_dimensions": config.default_dimensions
    }


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        model=config.default_model,
        version=config.app_version
    )


@app.post("/embed", response_model=EmbeddingResponse)
def generate_embedding(request: EmbeddingRequest):
    """
    Generate a 768-dimensional embedding for a single text input.
    
    - **text**: The text to generate embeddings for
    - **normalize**: Whether to normalize the embedding (recommended for similarity tasks)
    - **dimensions**: Output embedding dimensions (128-3072, default: 768)
    """
    try:
        result = embedding_service.generate_single_embedding(
            text=request.text,
            normalize=request.normalize,
            dimensions=request.dimensions
        )
        
        return EmbeddingResponse(**result)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate embedding: {str(e)}")


@app.post("/embed/batch", response_model=BatchEmbeddingResponse)
def generate_batch_embeddings(request: BatchEmbeddingRequest):
    """
    Generate embeddings for multiple texts in a single request.
    
    - **texts**: List of texts to generate embeddings for (max 100)
    - **normalize**: Whether to normalize the embeddings (recommended for similarity tasks)
    - **dimensions**: Output embedding dimensions (128-3072, default: 768)
    """
    try:
        # Validate batch size
        if len(request.texts) > config.max_batch_size:
            raise HTTPException(
                status_code=400, 
                detail=f"Batch size cannot exceed {config.max_batch_size} texts"
            )
        
        results = embedding_service.generate_batch_embeddings(
            texts=request.texts,
            normalize=request.normalize,
            dimensions=request.dimensions
        )
        
        embeddings = [EmbeddingResponse(**result) for result in results]
        
        return BatchEmbeddingResponse(
            embeddings=embeddings,
            total_count=len(embeddings)
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate batch embeddings: {str(e)}")


@app.post("/similarity", response_model=SimilarityResponse)
def calculate_similarity(request: SimilarityRequest):
    """
    Calculate cosine similarity between two texts.
    
    - **text1**: First text for comparison
    - **text2**: Second text for comparison
    - **normalize**: Whether to normalize embeddings before comparison
    """
    try:
        # Generate embeddings for both texts
        result1 = embedding_service.generate_single_embedding(
            text=request.text1,
            normalize=request.normalize
        )
        result2 = embedding_service.generate_single_embedding(
            text=request.text2,
            normalize=request.normalize
        )
        
        # Calculate similarity
        similarity = embedding_service.calculate_similarity(
            result1["embedding"],
            result2["embedding"]
        )
        
        return SimilarityResponse(
            text1=request.text1,
            text2=request.text2,
            similarity=similarity,
            embedding1=result1["embedding"],
            embedding2=result2["embedding"]
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate similarity: {str(e)}")


# Keep the old endpoint for backward compatibility
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """Legacy endpoint for backward compatibility."""
    return {"item_id": item_id, "q": q}

