# Docker Commands Guide for Insurance API (Chapter 8)

Quick reference for all Docker commands you'll need for this project.

## Setup Commands

```bash
# Verify Docker is installed
docker --version

# Login to Docker Hub
docker login

# Logout from Docker Hub
docker logout
```

## Building Images

```bash
# Build image with your username
docker build -t YOUR_USERNAME/insurance-api:1.0 .

# Build with specific Python version
docker build -t YOUR_USERNAME/insurance-api:1.0 --build-arg PYTHON_VERSION=3.10 .

# Build without cache (rebuild from scratch)
docker build --no-cache -t YOUR_USERNAME/insurance-api:1.0 .

# View build progress with verbose output
docker build --progress=plain -t YOUR_USERNAME/insurance-api:1.0 .
```

## Running Containers

```bash
# Run container in detached mode (background)
docker run -d -p 8000:8000 YOUR_USERNAME/insurance-api:1.0

# Run with specific name
docker run -d -p 8000:8000 --name insurance-api YOUR_USERNAME/insurance-api:1.0

# Run on different port
docker run -d -p 8001:8000 YOUR_USERNAME/insurance-api:1.0

# Run in interactive mode (for debugging)
docker run -it YOUR_USERNAME/insurance-api:1.0 /bin/bash

# Run with environment variables
docker run -d -p 8000:8000 -e API_VERSION=1.0 YOUR_USERNAME/insurance-api:1.0

# Run with volume mounting (for development)
docker run -d -p 8000:8000 -v /path/to/chapter7:/app YOUR_USERNAME/insurance-api:1.0

# Run with resource limits
docker run -d -p 8000:8000 --memory="512m" --cpus="1" YOUR_USERNAME/insurance-api:1.0

# Run multiple instances
docker run -d -p 8000:8000 --name api1 YOUR_USERNAME/insurance-api:1.0
docker run -d -p 8001:8000 --name api2 YOUR_USERNAME/insurance-api:1.0
```

## Managing Containers

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a running container
docker stop container_id
docker stop insurance-api

# Start a stopped container
docker start container_id

# Restart a container
docker restart container_id

# Remove a stopped container
docker rm container_id

# Remove container by name
docker rm insurance-api

# Force remove running container
docker rm -f insurance-api

# View container logs
docker logs container_id
docker logs insurance-api

# Follow logs in real-time
docker logs -f container_id

# View last 100 lines of logs
docker logs --tail 100 container_id

# Get container information
docker inspect container_id

# View container resource usage
docker stats container_id
```

## Managing Images

```bash
# List all images
docker images

# List images with filtering
docker images | grep insurance

# View image details
docker inspect image_id

# View image layers and history
docker history YOUR_USERNAME/insurance-api:1.0

# Tag an image with multiple names
docker tag YOUR_USERNAME/insurance-api:1.0 YOUR_USERNAME/insurance-api:latest

# Remove image
docker rmi image_id
docker rmi YOUR_USERNAME/insurance-api:1.0

# Remove multiple images
docker rmi image1 image2 image3

# Remove all unused images
docker image prune

# Remove all images (including used ones) - CAREFUL!
docker rmi $(docker images -q)

# Save image to file
docker save -o insurance-api.tar YOUR_USERNAME/insurance-api:1.0

# Load image from file
docker load -i insurance-api.tar
```

## Docker Hub Operations

```bash
# Push image to Docker Hub
docker push YOUR_USERNAME/insurance-api:1.0

# Push with latest tag
docker push YOUR_USERNAME/insurance-api:latest

# Pull image from Docker Hub
docker pull YOUR_USERNAME/insurance-api:1.0

# Search Docker Hub
docker search insurance-api

# View image info on Docker Hub
docker info YOUR_USERNAME/insurance-api:1.0
```

## Testing and Debugging

```bash
# Test API endpoint
curl http://localhost:8000

# Test health endpoint
curl http://localhost:8000/health

# Test predict endpoint with data
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 31,
    "weight": 91,
    "height": 1.72,
    "income_lpa": 10,
    "smoker": true,
    "city": "gurgaon",
    "occupation": "retired"
  }'

# Execute command inside running container
docker exec container_id python --version

# Open bash in running container
docker exec -it container_id /bin/bash

# Copy file from container to host
docker cp container_id:/app/file.txt ./file.txt

# Copy file from host to container
docker cp ./file.txt container_id:/app/file.txt

# View container's network
docker network inspect bridge
```

## Docker Compose Commands

```bash
# Start services defined in docker-compose.yml
docker-compose up

# Start in detached mode
docker-compose up -d

# Build and start
docker-compose up -d --build

# View running services
docker-compose ps

# View logs
docker-compose logs

# Follow logs for specific service
docker-compose logs -f insurance-api

# Stop all services
docker-compose stop

# Stop and remove containers
docker-compose down

# Remove everything including volumes
docker-compose down -v

# Restart services
docker-compose restart

# Execute command in service
docker-compose exec insurance-api python --version

# Scale service to multiple instances
docker-compose up -d --scale insurance-api=3
```

## Cleanup Commands

```bash
# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune

# Remove all unused volumes
docker volume prune

# Remove all unused networks
docker network prune

# Clean everything (CAUTION: removes stopped containers, unused images, networks, volumes)
docker system prune

# Remove everything and volumes (VERY CAUTION: removes all data!)
docker system prune -a --volumes
```

## Useful Aliases (add to .bashrc or .zshrc)

```bash
# Shortcuts for common commands
alias dk='docker'
alias dkb='docker build -t'
alias dkr='docker run -d -p'
alias dkps='docker ps'
alias dkl='docker logs -f'
alias dkrm='docker rm -f'

# Example usage:
# dkb YOUR_USERNAME/insurance-api:1.0 .
# dkr 8000:8000 YOUR_USERNAME/insurance-api:1.0
# dkl container_id
```

## Common Workflow

### For Developers

```bash
# 1. Make code changes
# 2. Build image
docker build -t YOUR_USERNAME/insurance-api:1.0 .

# 3. Run container
docker run -d -p 8000:8000 --name insurance-api YOUR_USERNAME/insurance-api:1.0

# 4. Test
curl http://localhost:8000/health

# 5. View logs
docker logs -f insurance-api

# 6. Make changes to code
# 7. Stop and remove
docker stop insurance-api
docker rm insurance-api

# 8. Rebuild and run
docker build -t YOUR_USERNAME/insurance-api:1.0 .
docker run -d -p 8000:8000 --name insurance-api YOUR_USERNAME/insurance-api:1.0
```

### For Publishing

```bash
# 1. Build final image
docker build -t YOUR_USERNAME/insurance-api:1.0 .

# 2. Test locally
docker run -d -p 8000:8000 --name test YOUR_USERNAME/insurance-api:1.0
curl http://localhost:8000/health
docker stop test
docker rm test

# 3. Login to Docker Hub
docker login

# 4. Push to Docker Hub
docker push YOUR_USERNAME/insurance-api:1.0

# 5. Verify on Docker Hub
# Visit https://hub.docker.com
```

### For Testing (Pull and Run)

```bash
# 1. Pull image from Docker Hub
docker pull YOUR_USERNAME/insurance-api:1.0

# 2. Run container
docker run -d -p 8000:8000 --name insurance-api YOUR_USERNAME/insurance-api:1.0

# 3. Test all endpoints
curl http://localhost:8000/docs

# 4. Cleanup
docker stop insurance-api
docker rm insurance-api
```

## Troubleshooting Commands

```bash
# Check if Docker daemon is running
docker ps

# View system information
docker info

# Diagnose issues
docker system df

# Check image build issues
docker build --progress=plain -t YOUR_USERNAME/insurance-api:1.0 .

# View container exit code
docker inspect -f '{{.State.ExitCode}}' container_id

# Restart Docker daemon (macOS)
osascript -e 'quit app "Docker"'
open -a Docker

# View all networks
docker network ls

# Inspect network
docker network inspect bridge
```

## Performance Tips

```bash
# Build with cache (faster)
docker build -t YOUR_USERNAME/insurance-api:1.0 .

# Use .dockerignore to reduce build context
# Already included in this project

# Multi-stage builds for smaller images
# See advanced Docker_Course materials

# Use specific Python version (smaller image)
FROM python:3.9-slim  # Good
FROM python:3.9      # Larger

# Regular cleanup
docker system prune
```

---

**Tip:** Most commands can be shortened:
- `docker ps` = `docker container ls`
- `docker images` = `docker image ls`
- `docker rmi` = `docker image rm`

**Note:** Replace `YOUR_USERNAME` with your actual Docker Hub username in all commands!
