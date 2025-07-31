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

### Deploy Latest Stable
```bash
docker run -d -p 8000:8000 ghcr.io/armanmaurya/embedding-generator-service:stable
```

### Update Docker Compose
```yaml
services:
  embedding-api:
    image: ghcr.io/armanmaurya/embedding-generator-service:v1.2.3
```

## 📋 Current Status

- **Current Version**: `1.0.1` (from VERSION file)
- **Workflow**: `.github/workflows/release.yml`
- **Registry**: `ghcr.io/armanmaurya/embedding-generator-service`

**Ready to create your first tag-based release!** 🎉
