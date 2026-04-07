#!/bin/bash

echo "🐳 Churn Prediction System - Docker Setup"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed!"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker installed: $(docker --version)"
echo "✅ Docker Compose installed: $(docker-compose --version)"
echo ""

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running!"
    echo "Please start Docker and try again."
    exit 1
fi

echo "✅ Docker daemon is running"
echo ""

# Navigate to deployment directory
cd "$(dirname "$0")"

echo "📦 Building Docker image..."
echo "This may take 5-10 minutes on first run..."
echo ""

docker-compose build

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Build failed! Check the error messages above."
    exit 1
fi

echo ""
echo "✅ Build successful!"
echo ""

echo "🚀 Starting application..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Failed to start! Check the error messages above."
    exit 1
fi

echo ""
echo "⏳ Waiting for application to be ready..."
sleep 10

# Test if application is responding
if curl -s http://localhost:8000/api/dashboard/metrics > /dev/null; then
    echo ""
    echo "✅ Application is running successfully!"
    echo ""
    echo "=========================================="
    echo "🎉 DEPLOYMENT COMPLETE!"
    echo "=========================================="
    echo ""
    echo "📊 Access your dashboard at:"
    echo "   http://localhost:8000"
    echo ""
    echo "📚 API Documentation:"
    echo "   http://localhost:8000/docs"
    echo ""
    echo "📋 Useful commands:"
    echo "   View logs:    docker-compose logs -f"
    echo "   Stop app:     docker-compose down"
    echo "   Restart:      docker-compose restart"
    echo ""
    echo "📖 For more info, see DOCKER_GUIDE.md"
    echo ""
else
    echo ""
    echo "⚠️  Application started but not responding yet."
    echo "   This is normal - it may take 30-60 seconds to initialize."
    echo ""
    echo "   Check status with: docker-compose logs -f"
    echo "   Then access: http://localhost:8000"
    echo ""
fi
