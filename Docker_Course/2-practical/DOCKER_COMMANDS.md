"""
Docker Commands Reference
All essential Docker commands explained
"""

# ============================================================================
# 1. IMAGE MANAGEMENT
# ============================================================================

# Build image from Dockerfile
docker build -t yourusername/appname:1.0 .
# -t: tag the image with name:version
# .: use Dockerfile in current directory

# Build with specific Dockerfile
docker build -f Dockerfile.ml -t yourusername/app:1.0 .

# List all images
docker images
docker image ls

# Search Docker Hub
docker search python

# Pull image from registry
docker pull ubuntu:20.04

# Push image to registry
docker login  # Login first
docker push yourusername/appname:1.0

# Remove image
docker rmi image_id
docker image rm yourusername/appname:1.0

# Remove all unused images
docker image prune

# Tag an existing image
docker tag old-name:old-tag new-name:new-tag

# Get image details
docker inspect image_id

# ============================================================================
# 2. CONTAINER MANAGEMENT
# ============================================================================

# Run container from image
docker run yourusername/appname:1.0

# Run with port mapping (-p)
docker run -p 8000:5000 yourusername/appname:1.0
# Accessible at: http://localhost:8000
# App inside listens on: 5000

# Run in detached mode (background)
docker run -d -p 8000:5000 yourusername/appname:1.0

# Run with name
docker run --name my-app -p 8000:5000 yourusername/appname:1.0

# Run with environment variables (-e)
docker run -e DEBUG=True -e API_KEY=secret yourusername/appname:1.0

# Run with volume mounting (-v)
docker run -v /path/on/host:/path/in/container yourusername/appname:1.0

# List running containers
docker ps
docker container ls

# List all containers (including stopped)
docker ps -a

# Stop container
docker stop container_id
docker stop container_name

# Start container
docker start container_id

# Restart container
docker restart container_id

# Pause container
docker pause container_id

# Unpause container
docker unpause container_id

# Remove container
docker rm container_id
docker rm container_name

# View container logs
docker logs container_id
docker logs -f container_id  # Follow logs (live)

# Execute command inside running container
docker exec -it container_id bash
docker exec -it container_id python script.py

# Get container details
docker inspect container_id

# Get container stats (CPU, memory)
docker stats container_id

# ============================================================================
# 3. DOCKER COMPOSE (Multiple Containers)
# ============================================================================

# Start all services in docker-compose.yml
docker-compose up
docker-compose up -d  # In background

# Stop all services
docker-compose down

# Remove services and volumes
docker-compose down -v

# View running services
docker-compose ps

# View logs
docker-compose logs
docker-compose logs -f  # Follow logs

# Rebuild images
docker-compose build

# ============================================================================
# 4. REGISTRY OPERATIONS
# ============================================================================

# Login to Docker Hub
docker login

# Logout
docker logout

# Search on Docker Hub
docker search redis

# ============================================================================
# 5. CLEANUP & MAINTENANCE
# ============================================================================

# Remove unused images
docker image prune

# Remove unused containers
docker container prune

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune
docker system prune -a  # Also removes images

# ============================================================================
# 6. DEBUGGING & INSPECTION
# ============================================================================

# Inspect image
docker inspect image_id

# Inspect container
docker inspect container_id

# View image history (layers)
docker history image_id

# Get container resource usage
docker stats

# ============================================================================
# USEFUL COMBINATIONS
# ============================================================================

# Build and run immediately
docker build -t myapp . && docker run -p 8000:5000 myapp

# Remove all stopped containers
docker container prune -f

# Remove image and associated containers
docker rmi $(docker images -q)

# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -aq)

# See logs of last 100 lines
docker logs --tail 100 container_id

# Follow logs with timestamps
docker logs -f --timestamps container_id

# ============================================================================
# DOCKER RUN FLAGS EXPLAINED
# ============================================================================

# -d           → Detached mode (background)
# -it          → Interactive terminal
# -p HOST:CONTAINER → Port mapping
# -e KEY=VALUE → Environment variable
# -v PATH      → Volume mounting
# --name       → Container name
# --network    → Connect to network
# --rm         → Auto-remove after stop
# --restart    → Restart policy
# -m 512m      → Memory limit
# --cpus 0.5   → CPU limit

# ============================================================================
# EXAMPLE COMPLETE WORKFLOW
# ============================================================================

# 1. Build image
docker build -t yourusername/myapp:1.0 .

# 2. Test locally
docker run -p 8000:5000 yourusername/myapp:1.0

# 3. Login to registry
docker login

# 4. Push to registry
docker push yourusername/myapp:1.0

# 5. On another machine: Pull and run
docker pull yourusername/myapp:1.0
docker run -d -p 8000:5000 yourusername/myapp:1.0

# 6. Monitor
docker ps
docker logs -f container_id

# 7. Stop
docker stop container_id

# ============================================================================
