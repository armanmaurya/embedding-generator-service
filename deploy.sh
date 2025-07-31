#!/bin/bash

# Build and Deploy Script for Embedding Generator API

set -e

echo "🚀 Embedding Generator API - Build & Deploy"
echo "=========================================="

# Function to display help
show_help() {
    echo "Usage: ./deploy.sh [OPTION]"
    echo ""
    echo "Options:"
    echo "  dev         Build and run development environment"
    echo "  prod        Build and run production environment"
    echo "  build       Build Docker images only"
    echo "  stop        Stop all containers"
    echo "  clean       Stop and remove containers, networks, and images"
    echo "  logs        Show container logs"
    echo "  help        Show this help message"
    echo ""
}

# Development deployment
deploy_dev() {
    echo "📦 Building development environment..."
    docker-compose -f docker-compose.dev.yml down
    docker-compose -f docker-compose.dev.yml build
    docker-compose -f docker-compose.dev.yml up -d
    echo "✅ Development environment is running on http://localhost:8000"
    echo "📖 API docs available at: http://localhost:8000/docs"
}

# Production deployment
deploy_prod() {
    echo "🏭 Building production environment..."
    docker-compose -f docker-compose.prod.yml down
    docker-compose -f docker-compose.prod.yml build
    docker-compose -f docker-compose.prod.yml up -d
    echo "✅ Production environment is running on http://localhost:8000"
    echo "📖 API docs available at: http://localhost:8000/docs"
}

# Build only
build_only() {
    echo "🔨 Building Docker images..."
    docker build -t embedding-generator:dev .
    docker build -t embedding-generator:prod -f Dockerfile.prod .
    echo "✅ Docker images built successfully"
}

# Stop containers
stop_containers() {
    echo "🛑 Stopping containers..."
    docker-compose -f docker-compose.yml down || true
    docker-compose -f docker-compose.dev.yml down || true
    docker-compose -f docker-compose.prod.yml down || true
    echo "✅ Containers stopped"
}

# Clean up
clean_up() {
    echo "🧹 Cleaning up Docker resources..."
    stop_containers
    docker system prune -f
    docker volume prune -f
    echo "✅ Cleanup completed"
}

# Show logs
show_logs() {
    echo "📋 Container logs:"
    echo "Development:"
    docker-compose -f docker-compose.dev.yml logs --tail=50 || echo "No dev containers running"
    echo ""
    echo "Production:"
    docker-compose -f docker-compose.prod.yml logs --tail=50 || echo "No prod containers running"
}

# Main script logic
case "${1:-help}" in
    "dev")
        deploy_dev
        ;;
    "prod")
        deploy_prod
        ;;
    "build")
        build_only
        ;;
    "stop")
        stop_containers
        ;;
    "clean")
        clean_up
        ;;
    "logs")
        show_logs
        ;;
    "help"|*)
        show_help
        ;;
esac
