# Embedding Generator API

A FastAPI-based service for generating 768-dimensional embeddings using Google's Gemini model.

## 📁 Project Structure

```
embedding-generator/
├── main.py                 # FastAPI application and route handlers
├── embedding_service.py    # Core embedding generation logic
├── models.py              # Pydantic models for request/response validation
├── config.py              # Configuration management
├── run_server.py          # Server startup script
├── gen_test.py            # Simple test script for embeddings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example          # Template for environment variables
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone <your-repo-url>
cd embedding-generator

# Create virtual environment
python -m venv env
env\Scripts\activate  # Windows
# source env/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy example environment file
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Edit .env file and add your Google AI API key
GOOGLE_AI_API_KEY=your_actual_api_key_here
```

### 3. Run the Server

```bash
# Option 1: Using the startup script
python run_server.py

# Option 2: Using uvicorn directly
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 📚 API Endpoints

### Base URL: `http://127.0.0.1:8000`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and available endpoints |
| `/health` | GET | Health check |
| `/embed` | POST | Generate single embedding |
| `/embed/batch` | POST | Generate multiple embeddings |
| `/similarity` | POST | Calculate similarity between two texts |
| `/docs` | GET | Interactive API documentation |

## 🔧 Usage Examples

### Single Embedding

```bash
curl -X POST "http://127.0.0.1:8000/embed" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "What is the meaning of life?",
       "normalize": true,
       "dimensions": 768
     }'
```

### Batch Embeddings

```bash
curl -X POST "http://127.0.0.1:8000/embed/batch" \
     -H "Content-Type: application/json" \
     -d '{
       "texts": ["Hello world", "How are you?", "Good morning"],
       "normalize": true,
       "dimensions": 768
     }'
```

### Text Similarity

```bash
curl -X POST "http://127.0.0.1:8000/similarity" \
     -H "Content-Type: application/json" \
     -d '{
       "text1": "I love programming",
       "text2": "I enjoy coding",
       "normalize": true
     }'
```

## 🏗️ Architecture

### Core Components

1. **`main.py`**: FastAPI application with route handlers
2. **`embedding_service.py`**: Embedding generation logic and utilities
3. **`models.py`**: Pydantic models for data validation
4. **`config.py`**: Configuration management and validation

### Key Features

- **Modular Design**: Separated concerns for maintainability
- **Environment Configuration**: All settings via environment variables
- **Input Validation**: Pydantic models ensure data integrity
- **Error Handling**: Comprehensive error handling and responses
- **Documentation**: Auto-generated OpenAPI documentation
- **Security**: API keys stored in environment variables

## ⚙️ Configuration

All configuration is handled via environment variables in `.env`:

```bash
# API Configuration
GOOGLE_AI_API_KEY=your_api_key

# App Configuration  
APP_NAME=Embedding Generator API
APP_VERSION=1.0.0

# Server Configuration
HOST=127.0.0.1
PORT=8000
RELOAD=true

# Embedding Configuration
EMBEDDING_MODEL=gemini-embedding-001
DEFAULT_DIMENSIONS=768
MAX_BATCH_SIZE=100
```

## 📊 Rate Limits (Google AI Free Tier)

- **Requests per minute**: 100
- **Tokens per minute**: 30,000
- **Requests per day**: 1,000
- **Cost**: Free

## 🔒 Security

- API keys stored in `.env` (not committed to git)
- Input validation on all endpoints
- Error handling prevents information leakage
- Rate limiting considerations for production

## 🧪 Testing

```bash
# Test basic functionality
python gen_test.py

# Test API health
curl http://127.0.0.1:8000/health

# View interactive documentation
# Open: http://127.0.0.1:8000/docs
```

## 📦 Dependencies

- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `pydantic`: Data validation
- `google-genai`: Google AI SDK
- `numpy`: Numerical operations
- `python-dotenv`: Environment variable management

## 🚀 Deployment

For production deployment, consider:

1. **Environment**: Use production ASGI server (Gunicorn + Uvicorn)
2. **Security**: Enable HTTPS, add authentication
3. **Monitoring**: Add logging, metrics, health checks
4. **Scaling**: Container deployment (Docker), load balancing
5. **Rate Limiting**: Implement proper rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Arman Maurya


