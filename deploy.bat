@echo off
REM Windows batch script for Docker deployment

echo 🚀 Embedding Generator API - Build ^& Deploy
echo ==========================================

if "%1"=="dev" goto dev
if "%1"=="prod" goto prod
if "%1"=="build" goto build
if "%1"=="stop" goto stop
if "%1"=="clean" goto clean
if "%1"=="logs" goto logs
goto help

:dev
echo 📦 Building development environment...
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up -d
echo ✅ Development environment is running on http://localhost:8000
echo 📖 API docs available at: http://localhost:8000/docs
goto end

:prod
echo 🏭 Building production environment...
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
echo ✅ Production environment is running on http://localhost:8000
echo 📖 API docs available at: http://localhost:8000/docs
goto end

:build
echo 🔨 Building Docker images...
docker build -t embedding-generator:dev .
docker build -t embedding-generator:prod -f Dockerfile.prod .
echo ✅ Docker images built successfully
goto end

:stop
echo 🛑 Stopping containers...
docker-compose -f docker-compose.yml down 2>nul
docker-compose -f docker-compose.dev.yml down 2>nul
docker-compose -f docker-compose.prod.yml down 2>nul
echo ✅ Containers stopped
goto end

:clean
echo 🧹 Cleaning up Docker resources...
call :stop
docker system prune -f
docker volume prune -f
echo ✅ Cleanup completed
goto end

:logs
echo 📋 Container logs:
echo Development:
docker-compose -f docker-compose.dev.yml logs --tail=50 2>nul || echo No dev containers running
echo.
echo Production:
docker-compose -f docker-compose.prod.yml logs --tail=50 2>nul || echo No prod containers running
goto end

:help
echo Usage: deploy.bat [OPTION]
echo.
echo Options:
echo   dev         Build and run development environment
echo   prod        Build and run production environment
echo   build       Build Docker images only
echo   stop        Stop all containers
echo   clean       Stop and remove containers, networks, and images
echo   logs        Show container logs
echo   help        Show this help message
echo.

:end
