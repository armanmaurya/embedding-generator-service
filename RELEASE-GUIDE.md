# 🏷️ Tag-Based Release System

## How It Works

Your embedding service uses a **simple tag-based release system**:

1. **Add a git tag** → Triggers automatic release
2. **GitHub Actions builds and pushes** Docker images  
3. **Creates GitHub release** with changelog

## 🚀 Creating a Release

```bash
# Create and push a tag
git tag v1.0.2
git push origin v1.0.2
```

## 📦 Generated Docker Images

When you push a tag like `v1.2.3`, you get these images:

- `ghcr.io/armanmaurya/embedding-generator-service:v1.2.3` (exact version)
- `ghcr.io/armanmaurya/embedding-generator-service:v1.2` (major.minor)
- `ghcr.io/armanmaurya/embedding-generator-service:v1` (major only)
- `ghcr.io/armanmaurya/embedding-generator-service:latest` (always latest)
- `ghcr.io/armanmaurya/embedding-generator-service:stable` (stable release)

## 🔧 Release Workflow Features

- ✅ **Builds production Docker image** using `Dockerfile.prod`
- ✅ **Multi-tag strategy** for flexible deployments
- ✅ **GitHub release creation** with automatic changelog
- ✅ **Container registry push** to GHCR
- ✅ **Docker build caching** for faster builds

## 🎯 Usage Examples

### Deploy Specific Version
```bash
docker run -d -p 8000:8000 ghcr.io/armanmaurya/embedding-generator-service:v1.2.3
```

### Deploy with Environment Variables
```bash
# Using .env file (recommended)
docker run -d -p 8000:8000 --env-file .env ghcr.io/armanmaurya/embedding-generator-service:v1.2.3

# Or pass individual environment variables
docker run -d -p 8000:8000 \
  -e GOOGLE_AI_API_KEY=your_api_key \
  -e EMBEDDING_MODEL=gemini-embedding-001 \
  ghcr.io/armanmaurya/embedding-generator-service:v1.2.3
```

### Deploy Latest Stable
```bash
docker run -d -p 8000:8000 --env-file .env ghcr.io/armanmaurya/embedding-generator-service:stable
```

### Update Docker Compose
```yaml
services:
  embedding-api:
    image: ghcr.io/armanmaurya/embedding-generator-service:v1.2.3
    env_file:
      - .env
    ports:
      - "8000:8000"
```

## 📋 Current Status

- **Current Version**: `1.0.4` (from VERSION file)
- **Workflow**: `.github/workflows/release.yml`
- **Registry**: `ghcr.io/armanmaurya/embedding-generator-service`

## 🔧 Environment Configuration

The service requires environment variables for proper operation. Create a `.env` file with:

```properties
# Google AI API Configuration
GOOGLE_AI_API_KEY=your_google_ai_api_key

# FastAPI Configuration
APP_NAME=Embedding Generator API
APP_DESCRIPTION=Generate 768-dimensional embeddings using Googles Gemini model
APP_VERSION=1.0.0

# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=false

# Embedding Configuration
EMBEDDING_MODEL=gemini-embedding-001
DEFAULT_DIMENSIONS=768
MAX_BATCH_SIZE=100

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
```

**Ready to create your first tag-based release!** 🎉
