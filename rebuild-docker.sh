#!/bin/bash
# Docker Development Rebuild Script (Linux/Mac)
# Use this script when you make changes to your code

echo "🔄 Stopping and removing current container..."
docker stop teaching-app
docker rm teaching-app

echo "🏗️ Rebuilding Docker image..."
docker build -t teaching-fullstack .

echo "🚀 Starting new container..."
docker run -d --name teaching-app -p 8000:8000 -p 5173:5173 -v $(pwd)/teaching/db.sqlite3:/app/teaching/db.sqlite3 teaching-fullstack

echo "📋 Running containers:"
docker ps

echo "📜 Container logs:"
docker logs teaching-app
