"""
FastAPI Embedding Generator API

Main application file that defines API routes and handles HTTP requests.

MIT License
Copyright (c) 2025 Arman Maurya
"""

from typing import Union
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import requests as http_requests
import json
import base64

# Import our custom modules
from .config import config
from .embedding_service import EmbeddingService
from .models import (
    ArticleEmbeddingRequest,
    ArticleEmbeddingResponse,
    CloudTasksPayload,
    EmbeddingRequest,
    EmbeddingResponse,
    HealthResponse,
    ErrorResponse,
)

# Validate configuration
if not config.validate():
    raise RuntimeError(
        "Invalid configuration. Please check your environment variables."
    )

# Initialize FastAPI app with config
app = FastAPI(**config.get_fastapi_config())

# Initialize embedding service
embedding_service = EmbeddingService(api_key=config.google_ai_api_key)


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"Internal server error: {str(exc)}",
            "error_type": "InternalServerError",
        },
    )


@app.get("/", response_model=dict)
def read_root():
    """Root endpoint with API information."""
    return {
        "message": config.app_name,
        "version": config.app_version,
        "endpoints": {
            "/embed": "Generate single embedding",
            "/article/embed": "Generate embedding for an article and save",
            "/tasks/embed": "Process embedding generation from Google Cloud Tasks",
            "/tasks/embed-raw": "Process embedding generation from Google Cloud Tasks (raw format)",
            "/health": "Health check",
            "/docs": "API documentation",
        },
        "model": config.default_model,
        "default_dimensions": config.default_dimensions,
    }


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy", model=config.default_model, version=config.app_version
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
            dimensions=request.dimensions,
        )
        return EmbeddingResponse(**result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate embedding: {str(e)}"
        )

@app.post("/article/embed", response_model=ArticleEmbeddingResponse)
def generate_article_embedding(request: ArticleEmbeddingRequest):
    """
    Generate embedding for an article.

    - **article_id**: Unique identifier for the article
    - **text**: The text content of the article
    - **normalize**: Whether to normalize the embedding vector
    - **dimensions**: Output embedding dimensions (128-3072, default: 768)
    """
    try:
        result = embedding_service.generate_single_embedding(
            text=request.text,
            normalize=request.normalize,
            dimensions=request.dimensions,
        )
        response = http_requests.post(
            config.save_embedding_api_endpoint,
            json={
                "article_id": request.article_id,
                "embedding": result["embedding"],
                "dimension": result["dimension"],
                "normalized": result["normalized"],
                "model": result["model"],
            },
        )
        if response.status_code != 200:
            raise Exception(f"Failed to save embedding: {response.text}")
        return ArticleEmbeddingResponse(status="success", article_id=request.article_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate article embedding: {str(e)}"
        )


@app.post("/tasks/embed", response_model=ArticleEmbeddingResponse)
def process_cloud_task_embedding(payload: CloudTasksPayload):
    """
    Process embedding generation requests from Google Cloud Tasks.
    
    This endpoint expects the Google Cloud Tasks payload format with:
    - task_type: Type of task (should be 'embedding_generation')
    - timestamp: Task creation timestamp
    - article_embedding_request: The actual embedding request data
    """
    try:
        print(f"Received Cloud Tasks payload: {payload}")
        print(f"Task type: {payload.task_type}")
        print(f"Article request: {payload.article_embedding_request}")
        
        # Validate task type
        if payload.task_type != 'embedding_generation':
            print(f"Invalid task type received: {payload.task_type}")
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid task type: {payload.task_type}. Expected 'embedding_generation'"
            )
        
        # Extract the article embedding request
        request = payload.article_embedding_request
        print(f"Extracted request - Article ID: {request.article_id}, Text length: {len(request.text)}")
        
        # Generate the embedding
        result = embedding_service.generate_single_embedding(
            text=request.text,
            normalize=request.normalize,
            dimensions=request.dimensions,
        )
        print(f"Generated embedding with dimension: {result['dimension']}")
        
        # Save the embedding to the external API
        save_payload = {
            "article_id": request.article_id,
            "embedding": result["embedding"],
            "dimension": result["dimension"],
            "normalized": result["normalized"],
            "model": result["model"],
        }
        print(f"Sending to save API: {config.save_embedding_api_endpoint}")
        
        response = http_requests.post(
            config.save_embedding_api_endpoint,
            json=save_payload,
        )
        
        print(f"Save API response status: {response.status_code}")
        if response.status_code != 200:
            print(f"Save API error response: {response.text}")
            raise Exception(f"Failed to save embedding: {response.text}")
            
        print(f"Successfully processed embedding for article: {request.article_id}")
        return ArticleEmbeddingResponse(status="success", article_id=request.article_id)

    except ValueError as e:
        print(f"ValueError in cloud task processing: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Exception in cloud task processing: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to process cloud task embedding: {str(e)}"
        )


@app.post("/tasks/embed-raw")
async def process_cloud_task_embedding_raw(request: Request):
    """
    Process embedding generation requests from Google Cloud Tasks (raw format).
    
    This endpoint handles the raw Google Cloud Tasks request and attempts to parse it.
    """
    try:
        print("=== Raw Cloud Tasks Request ===")
        # Get the raw body
        body = await request.body()
        print(f"Raw body type: {type(body)}, length: {len(body)}")
        print(f"Raw body (first 200 chars): {body[:200]}")
        
        # Try to decode if it's base64 encoded
        try:
            # Google Cloud Tasks sends base64 encoded body
            decoded_body = base64.b64decode(body).decode('utf-8')
            print(f"Successfully decoded base64. Decoded length: {len(decoded_body)}")
            print(f"Decoded body (first 200 chars): {decoded_body[:200]}")
            payload_data = json.loads(decoded_body)
            print("Successfully parsed JSON from base64 decoded body")
        except Exception as decode_error:
            print(f"Base64 decode failed: {decode_error}")
            # If not base64, try to parse as JSON directly
            try:
                payload_data = json.loads(body.decode('utf-8'))
                print("Successfully parsed JSON from raw body")
            except Exception as json_error:
                # If still fails, log what we received
                print(f"JSON parse failed: {json_error}")
                print(f"Raw body received: {body}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Unable to parse request body. Raw body: {body[:500]}"
                )
        
        print(f"Parsed payload: {payload_data}")
        
        # Validate task type
        if payload_data.get('task_type') != 'embedding_generation':
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid task type: {payload_data.get('task_type')}. Expected 'embedding_generation'"
            )
        
        # Extract the article embedding request
        article_request = payload_data.get('article_embedding_request')
        if not article_request:
            raise HTTPException(
                status_code=400,
                detail="Missing article_embedding_request in payload"
            )
        
        # Generate the embedding
        result = embedding_service.generate_single_embedding(
            text=article_request.get('text'),
            normalize=article_request.get('normalize', True),
            dimensions=article_request.get('dimensions', 768),
        )
        
        # Save the embedding to the external API
        response = http_requests.post(
            config.save_embedding_api_endpoint,
            json={
                "article_id": article_request.get('article_id'),
                "embedding": result["embedding"],
                "dimension": result["dimension"],
                "normalized": result["normalized"],
                "model": result["model"],
            },
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to save embedding: {response.text}")
            
        return {
            "status": "success", 
            "article_id": article_request.get('article_id')
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing cloud task: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to process cloud task embedding: {str(e)}"
        )


# Keep the old endpoint for backward compatibility
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """Legacy endpoint for backward compatibility."""
    return {"item_id": item_id, "q": q}
