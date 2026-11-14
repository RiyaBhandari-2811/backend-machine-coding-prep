# Docker Quick Reference & Cheatsheet

## Image Commands

```bash
# Build image
docker build -t username/appname:1.0 .
docker build -f Dockerfile.prod -t app:prod .

# List images
docker images
docker image ls -a

# Remove image
docker rmi image_id
docker image rm username/appname:1.0

# Search Docker Hub
docker search python
docker search ubuntu:20.04

# Pull image
docker pull ubuntu:20.04
docker pull username/myapp:latest

# Push image
docker login
docker push username/myapp:1.0

# Tag image
docker tag old:tag new:tag
docker tag myapp:1.0 username/myapp:1.0

# Inspect image
docker inspect image_id
docker inspect --format='{{.Architecture}}' image_id

# History (layers)
docker history image_id
```

---

## Container Commands

```bash
# Run container
docker run image:tag
docker run -d -p 8000:5000 --name myapp image:tag

# List containers
docker ps                    # Running only
docker ps -a                 # All containers

# Stop/Start
docker stop container_id
docker start container_id
docker restart container_id

# Remove container
docker rm container_id
docker rm $(docker ps -aq)   # All containers

# Logs
docker logs container_id
docker logs -f container_id              # Follow
docker logs --tail 100 container_id      # Last 100 lines
docker logs --timestamps container_id

# Execute command
docker exec -it container_id bash
docker exec -it container_id python script.py

# Pause/Unpause
docker pause container_id
docker unpause container_id

# Get container info
docker inspect container_id
docker stats container_id    # CPU, memory, network I/O
docker top container_id      # Running processes
```

---

## Common Run Flags

```bash
# Port mapping
docker run -p 8000:5000 app:tag
docker run -p 8000:5000 -p 8001:5001 app:tag

# Detach mode (background)
docker run -d app:tag

# Interactive terminal
docker run -it app:tag bash

# Environment variables
docker run -e DEBUG=True -e PORT=5000 app:tag

# Volume mounting
docker run -v /host/path:/container/path app:tag
docker run -v data:/app/data app:tag          # Named volume

# Container name
docker run --name myapp app:tag

# Network
docker run --network mynetwork app:tag

# Resource limits
docker run -m 512m --cpus 0.5 app:tag

# Auto-remove
docker run --rm app:tag

# Restart policy
docker run --restart=always app:tag
docker run --restart=on-failure:3 app:tag

# Background + port + name
docker run -d -p 8000:5000 --name myapp app:tag
```

---

## Docker Compose

```bash
# Start services
docker-compose up
docker-compose up -d         # Background

# Stop services
docker-compose down
docker-compose down -v       # Remove volumes

# List services
docker-compose ps

# View logs
docker-compose logs
docker-compose logs -f       # Follow
docker-compose logs service_name

# Build images
docker-compose build
docker-compose build --no-cache

# Execute command
docker-compose exec service_name bash
docker-compose exec service_name python script.py

# Restart services
docker-compose restart
docker-compose restart service_name

# Remove specific service
docker-compose rm service_name
```

---

## Network Commands

```bash
# List networks
docker network ls

# Create network
docker network create mynetwork

# Remove network
docker network rm mynetwork

# Inspect network
docker network inspect mynetwork

# Connect container to network
docker network connect mynetwork container_id

# Disconnect
docker network disconnect mynetwork container_id
```

---

## Volume Commands

```bash
# List volumes
docker volume ls

# Create volume
docker volume create myvolume

# Remove volume
docker volume rm myvolume

# Inspect volume
docker volume inspect myvolume

# Prune unused volumes
docker volume prune

# Mount volume
docker run -v myvolume:/app/data app:tag
docker run -v /host/path:/app/data app:tag
```

---

## Cleanup & Maintenance

```bash
# Remove unused images
docker image prune
docker image prune -a        # Remove all unused

# Remove unused containers
docker container prune

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Clean everything
docker system prune
docker system prune -a       # Include all images

# Disk usage
docker system df

# Clean space
docker builder prune
```

---

## Debugging

```bash
# View logs
docker logs container_id

# Follow logs
docker logs -f container_id

# Last N lines
docker logs --tail 50 container_id

# With timestamps
docker logs --timestamps container_id

# Since specific time
docker logs --since 2024-01-01T00:00:00 container_id

# Get shell access
docker exec -it container_id bash
docker exec -it container_id sh   # Alpine

# Check processes
docker top container_id

# Monitor resources
docker stats

# Inspect everything
docker inspect container_id
docker inspect image_id
```

---

## Dockerfile Basics

```dockerfile
# Base image
FROM python:3.9

# Working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variable
ENV DEBUG=True

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s CMD curl -f http://localhost:5000/health || exit 1

# Default command
CMD ["python", "app.py"]

# Entry point
ENTRYPOINT ["python", "app.py"]
```

---

## .dockerignore

```
# Git
.git
.gitignore

# Python
__pycache__
*.pyc
venv/
env/
.env

# Node
node_modules/

# IDEs
.vscode
.idea

# OS
.DS_Store
Thumbs.db

# Build
build/
dist/

# Logs
*.log

# Tests
.pytest_cache
.coverage
```

---

## docker-compose.yml Basics

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:5000"
    environment:
      - DEBUG=True
    volumes:
      - ./app:/app
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:

networks:
  default:
```

---

## Common Workflows

### Build & Test Locally

```bash
# 1. Build
docker build -t myapp:dev .

# 2. Run
docker run -d -p 8000:5000 --name myapp myapp:dev

# 3. Test
curl http://localhost:8000

# 4. View logs
docker logs myapp

# 5. Execute command
docker exec myapp python script.py

# 6. Stop
docker stop myapp

# 7. Remove
docker rm myapp
```

### Build, Tag, Push to Registry

```bash
# 1. Build
docker build -t myapp:1.0 .

# 2. Tag for registry
docker tag myapp:1.0 username/myapp:1.0

# 3. Login
docker login

# 4. Push
docker push username/myapp:1.0

# 5. Verify on Docker Hub
# Visit: hub.docker.com/username
```

### Pull & Run from Registry

```bash
# 1. Pull
docker pull username/myapp:1.0

# 2. Run
docker run -d -p 8000:5000 username/myapp:1.0

# 3. Access
# Visit: http://localhost:8000
```

### Multi-container with Compose

```bash
# 1. Create docker-compose.yml (see template above)

# 2. Start all services
docker-compose up -d

# 3. Check status
docker-compose ps

# 4. View logs
docker-compose logs -f

# 5. Access services
# Web: http://localhost:8000
# DB: localhost:5432

# 6. Stop all
docker-compose down
```

---

## Problem Solving Quick Reference

| Problem | Solution |
|---------|----------|
| Port already in use | Use different port: `-p 8001:5000` |
| Container not starting | Check logs: `docker logs container_id` |
| Can't connect to DB | Ensure services linked, use service name |
| Image too large | Use slim base image: `python:3.9-slim` |
| Build slow | Use `.dockerignore`, multi-stage build |
| Permissions denied | Add to docker group: `usermod -aG docker $USER` |
| Out of disk space | Run: `docker system prune -a` |
| Environment vars not set | Pass with `-e` or in docker-compose.yml |
| Volume not mounting | Check path syntax, use `docker inspect` |
| Container keeps restarting | Check exit code: `docker logs container_id` |

---

## Environment Variables Cheatsheet

### In Dockerfile
```dockerfile
ENV DEBUG=True
ENV API_KEY=default_key
ENV PORT=5000
```

### At Runtime
```bash
docker run -e DEBUG=True -e API_KEY=secret app:tag
```

### In docker-compose.yml
```yaml
services:
  app:
    environment:
      - DEBUG=True
      - API_KEY=secret
      - PORT=5000
```

### In .env file
```bash
DEBUG=True
API_KEY=secret
PORT=5000
```

Then in docker-compose.yml:
```yaml
env_file:
  - .env
```

---

## Network Modes

```bash
# Bridge (default)
docker run app:tag

# Host (Linux only)
docker run --network host app:tag

# None (no network)
docker run --network none app:tag

# Custom network
docker network create mynet
docker run --network mynet app:tag
```

---

## Restart Policies

```bash
# No restart
docker run app:tag

# Always restart
docker run --restart=always app:tag

# Restart on failure (max 3 times)
docker run --restart=on-failure:3 app:tag

# Unless stopped
docker run --restart=unless-stopped app:tag
```

---

## Useful One-liners

```bash
# Stop all containers
docker stop $(docker ps -q)

# Remove all stopped containers
docker container prune -f

# Remove all images
docker rmi $(docker images -q)

# Get container IP
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_id

# Get container port mapping
docker port container_id

# Watch container stats live
docker stats --no-stream=false

# Remove dangling images
docker image prune -f
```

---

## Key Points to Remember

✅ Image = Blueprint, Container = Running instance  
✅ `-p host:container` = Port mapping  
✅ `-v path:/path` = Volume mounting  
✅ `-e KEY=VALUE` = Environment variables  
✅ `-d` = Detached (background)  
✅ `-it` = Interactive terminal  
✅ `docker-compose up -d` = Start multi-container app  
✅ Always use specific version tags (not `latest`)  

---

**Save this for quick reference during work!** 📌
