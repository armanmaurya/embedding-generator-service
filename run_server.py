#!/usr/bin/env python3
"""
Server startup script for the Embedding Generator API.

MIT License
Copyright (c) 2025 Arman Maurya
"""

import uvicorn
from config import config

if __name__ == "__main__":
    print(f"Starting {config.app_name} v{config.app_version}")
    print(f"Running on http://{config.host}:{config.port}")
    print(f"Using model: {config.default_model}")
    print(f"API documentation: http://{config.host}:{config.port}/docs")
    
    # Run the server
    uvicorn.run(
        "main:app",
        **config.get_uvicorn_config()
    )
