# Docker Development Rebuild Script
# Use this script when you make changes to your code

# Stop and remove current container
docker stop teaching-app
docker rm teaching-app

# Rebuild the image
docker build -t teaching-fullstack .

# Start new container with both ports
docker run -d --name teaching-app -p 8000:8000 -p 5173:5173 -v ${PWD}/teaching/db.sqlite3:/app/teaching/db.sqlite3 teaching-fullstack

# Show running containers
docker ps

# Show logs
echo "=== Container Logs ==="
docker logs teaching-app
