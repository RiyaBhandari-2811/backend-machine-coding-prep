# Docker Interview Questions & Answers

## Level: Beginner

### Q1: What is Docker and why do we need it?

**Answer:**
Docker is a containerization platform that helps developers build, ship, and run applications in isolated environments called containers.

**Why we need it:**
1. **Consistency:** Code works identically on dev/test/prod
2. **Isolation:** Multiple apps on same server without conflicts
3. **Scalability:** Easy to run multiple instances
4. **Efficiency:** Lightweight compared to VMs
5. **Deployment:** Simple, reliable application delivery

**Real analogy:** Like Maggi noodles - pre-packaged with all ingredients, same taste everywhere.

---

### Q2: What is the difference between a Docker image and a Docker container?

**Answer:**

| Aspect | Image | Container |
|--------|-------|-----------|
| Type | Blueprint/Template | Running instance |
| Analogy | DVD of a movie | Movie playing on TV |
| State | Static | Dynamic |
| Creation | Built from Dockerfile | Created from image |
| Persistence | Persistent | Temporary (unless volume used) |
| Multiple instances | Yes, multiple containers from one image | Each is independent |

**Example:**
- Image: `python:3.9` (template)
- Container: Running Python environment using that image (instance)

---

### Q3: What is a Dockerfile?

**Answer:**
A text file containing instructions to build a Docker image. Each instruction creates a layer in the image.

**Basic structure:**
```dockerfile
FROM python:3.9              # Base image
WORKDIR /app                 # Working directory
COPY . /app                  # Copy files
RUN pip install -r requirements.txt  # Install dependencies
EXPOSE 5000                  # Expose port
CMD ["python", "app.py"]     # Default command
```

**Key instructions:**
- `FROM:` Base image to start with
- `WORKDIR:` Set working directory
- `COPY/ADD:` Copy files
- `RUN:` Execute command during build
- `EXPOSE:` Document port
- `CMD:` Default command when container starts

---

### Q4: Explain port mapping with an example.

**Answer:**
Port mapping connects a port inside the container to a port on your machine.

**Syntax:** `-p HOST_PORT:CONTAINER_PORT`

**Example:**
```bash
docker run -p 8000:5000 myapp:1.0
           └─────┬────┘ └─┬──┘
            your machine  inside
            (localhost:8000)  container
```

**What happens:**
- Your machine: Access app at `http://localhost:8000`
- Container: App actually listens on port 5000
- Mapping: Docker redirects 8000 → 5000

**Why needed:**
- Your machine might already use port 5000
- Multiple containers can't use same port on host
- Allows running multiple instances (8001, 8002, etc.)

---

### Q5: What is Docker Hub and how do you use it?

**Answer:**
Docker Hub is a public registry (like GitHub for images) where developers store and share Docker images.

**Website:** hub.docker.com

**Key features:**
- **Public images:** Anyone can access (python, ubuntu, nodejs, etc.)
- **Private repositories:** Only your team can access
- **Official images:** Docker-verified, high quality
- **Tagging:** Same image with different versions (latest, v1.0, v2.0)

**Usage:**
```bash
# 1. Login
docker login

# 2. Pull image
docker pull python:3.9
docker pull username/myapp:1.0

# 3. Push your image
docker tag myapp:1.0 username/myapp:1.0
docker push username/myapp:1.0

# 4. Others can pull
docker pull username/myapp:1.0
```

---

### Q6: How do you build a Docker image?

**Answer:**
Using the `docker build` command with a Dockerfile.

**Command:**
```bash
docker build -t username/appname:1.0 .
            └─┬─┘         └───┬────┘  └─┬─┘
            option          tag      context
            (tag name)    (optional)  (Dockerfile location)
```

**Process:**
1. Docker reads Dockerfile
2. Executes each instruction (creates a layer)
3. Caches layers for faster rebuilds
4. Creates final image

**Example:**
```bash
# Build from Dockerfile in current directory
docker build -t myapp:1.0 .

# Build from specific Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# Build without cache (force rebuild)
docker build --no-cache -t myapp:1.0 .
```

---

### Q7: What's the difference between Docker and Virtual Machines?

**Answer:**

| Aspect | Docker | Virtual Machine |
|--------|--------|-----------------|
| Size | ~MB to few GB | ~GB (full OS) |
| Startup time | Seconds | Minutes |
| Resource usage | Lightweight | Heavy |
| OS | Shares host OS | Full OS included |
| Performance | Near native | Slower |
| Isolation | Process level | Machine level |
| Scalability | Excellent | Good |
| Boot speed | Fast | Slow |

**Visual:**
```
Docker:
Host OS
├─ Docker Engine
├─ Container 1 (app + libs)
├─ Container 2 (app + libs)
└─ Container 3 (app + libs)
(Shared kernel)

VM:
Host OS
├─ Hypervisor
├─ Full OS + Container 1
├─ Full OS + Container 2
└─ Full OS + Container 3
(Each has full OS)
```

---

### Q8: How do you run a Docker container?

**Answer:**
Using `docker run` command.

**Basic syntax:**
```bash
docker run [OPTIONS] IMAGE [COMMAND]
```

**Common examples:**
```bash
# Simple run
docker run ubuntu:20.04

# Run with port mapping
docker run -p 8000:5000 myapp:1.0

# Run in background (detached)
docker run -d -p 8000:5000 myapp:1.0

# Run with interactive terminal
docker run -it ubuntu:20.04 bash

# Run with environment variables
docker run -e DEBUG=True -e PORT=5000 myapp:1.0

# Run with name
docker run --name myapp -p 8000:5000 myapp:1.0

# Run with volume
docker run -v /data:/app/data myapp:1.0
```

**Key flags:**
- `-d` = Detached (background)
- `-it` = Interactive terminal
- `-p` = Port mapping
- `-e` = Environment variable
- `--name` = Container name
- `-v` = Volume mounting

---

### Q9: What's the difference between CMD and ENTRYPOINT?

**Answer:**

| Aspect | CMD | ENTRYPOINT |
|--------|-----|-----------|
| Purpose | Default command | Configure as executable |
| Override | Easy (command replaces CMD) | Harder (command is arg) |
| Common use | Application logic | Wrapper/initialization |
| Combination | Can combine both | Often with CMD |

**Examples:**

**Using CMD (easy to override):**
```dockerfile
CMD ["python", "app.py"]
```
```bash
docker run myapp:1.0              # Runs: python app.py
docker run myapp:1.0 bash         # Runs: bash (overrides)
```

**Using ENTRYPOINT (harder to override):**
```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]
```
```bash
docker run myapp:1.0              # Runs: python app.py
docker run myapp:1.0 --help       # Runs: python --help
```

---

### Q10: How do you view Docker logs?

**Answer:**
Using `docker logs` command.

**Examples:**
```bash
# View all logs
docker logs container_id

# Follow logs (live)
docker logs -f container_id

# Last 50 lines
docker logs --tail 50 container_id

# With timestamps
docker logs --timestamps container_id

# Since specific time
docker logs --since 2024-01-01T00:00:00 container_id

# Until specific time
docker logs --until 2024-01-02T00:00:00 container_id
```

**Useful patterns:**
```bash
# Watch logs in real-time
docker logs -f container_id

# Check error in last 100 lines
docker logs --tail 100 container_id | grep ERROR

# Save logs to file
docker logs container_id > app.log
```

---

## Level: Intermediate

### Q11: What is Docker Compose and why use it?

**Answer:**
Docker Compose is a tool for defining and running multi-container applications.

**Why use it:**
1. **Simplicity:** Define all services in one file
2. **Dependencies:** Manage service startup order
3. **Networking:** Automatic network creation
4. **Volumes:** Easy data persistence
5. **One-command:** `docker-compose up` starts everything

**Example docker-compose.yml:**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:5000"
  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
```

**Usage:**
```bash
docker-compose up -d      # Start all services
docker-compose ps         # List services
docker-compose logs -f    # View logs
docker-compose down       # Stop all services
```

---

### Q12: Explain Docker networking.

**Answer:**
Docker provides networking so containers can communicate with each other.

**Network types:**
1. **Bridge (default):** Isolated network, containers can communicate
2. **Host:** Container uses host's network (Linux only)
3. **None:** No network
4. **Custom bridge:** User-defined network

**Example:**
```bash
# Create network
docker network create mynet

# Run containers on same network
docker run --network mynet --name web myapp:1.0
docker run --network mynet --name db postgres:13

# Inside containers, communicate by name:
# web can connect to: db:5432
```

**In docker-compose (automatic):**
```yaml
services:
  web:
    # Can access db as: db:5432
  db:
    image: postgres
    # Can access web by service name
```

---

### Q13: What are Docker volumes and why use them?

**Answer:**
Volumes persist data outside containers so it's not lost when container stops.

**Three types:**
1. **Named volumes:** Managed by Docker
2. **Bind mounts:** Link host directory to container
3. **tmpfs:** In-memory storage (temporary)

**Examples:**
```bash
# Named volume
docker volume create mydata
docker run -v mydata:/app/data myapp:1.0

# Bind mount
docker run -v /host/path:/container/path myapp:1.0

# tmpfs (ephemeral)
docker run --tmpfs /app/temp myapp:1.0
```

**In docker-compose:**
```yaml
services:
  app:
    volumes:
      - mydata:/app/data

volumes:
  mydata:
```

**Why:**
- ✅ Data persists after container removal
- ✅ Easy data sharing between containers
- ✅ Performance optimization
- ✅ Database persistence

---

### Q14: How do you reduce Docker image size?

**Answer:**
Several strategies:

**1. Use slim base images:**
```dockerfile
# Before: 900MB
FROM python:3.9

# After: ~150MB
FROM python:3.9-slim

# Ultra lightweight: ~50MB
FROM python:3.9-alpine
```

**2. Multi-stage builds:**
```dockerfile
# Stage 1: Build
FROM python:3.9 AS builder
RUN pip install -r requirements.txt

# Stage 2: Runtime (only copies artifacts)
FROM python:3.9-slim
COPY --from=builder /dependencies /dependencies
```

**3. Minimize layers:**
```dockerfile
# Bad (3 layers)
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# Good (1 layer)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
```

**4. Use .dockerignore:**
```
__pycache__
venv/
.git
node_modules
```

**5. Remove unnecessary dependencies:**
```dockerfile
# Don't install dev dependencies in production
RUN pip install --no-deps production_libs
```

---

### Q15: What's a health check in Docker?

**Answer:**
A health check ensures container is actually healthy (not just running).

**In Dockerfile:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1
```

**Flags:**
- `--interval`: Check every N seconds
- `--timeout`: Wait N seconds for response
- `--retries`: Fail after N failures
- `--start-period`: Grace period before first check

**Status:**
```bash
docker inspect container_id
# Shows: "State": {"Health": "healthy"/"unhealthy"}
```

**Usage:**
- Docker Swarm: Remove unhealthy containers
- Kubernetes: Readiness/liveness probes
- Monitoring: Alert on health changes

---

### Q16: How do you pass environment variables to Docker containers?

**Answer:**
Multiple ways:

**1. Command line:**
```bash
docker run -e DEBUG=True -e PORT=5000 myapp:1.0
```

**2. .env file:**
```bash
# .env
DEBUG=True
PORT=5000
```
```bash
docker run --env-file .env myapp:1.0
```

**3. In Dockerfile:**
```dockerfile
ENV DEBUG=True
ENV PORT=5000
```

**4. docker-compose.yml:**
```yaml
services:
  app:
    environment:
      - DEBUG=True
      - PORT=5000
    # Or:
    env_file:
      - .env
```

**Access in Python:**
```python
import os
debug = os.getenv('DEBUG', 'False')
port = os.getenv('PORT', '5000')
```

**Security:** Don't hardcode secrets in Dockerfile. Use:
```bash
docker run -e API_KEY=$API_KEY myapp:1.0  # From host env
```

---

### Q17: What does `docker exec` do?

**Answer:**
Execute a command inside a running container.

**Syntax:**
```bash
docker exec [OPTIONS] CONTAINER COMMAND
```

**Common examples:**
```bash
# Open bash shell
docker exec -it container_id bash

# Run Python script
docker exec container_id python script.py

# Check files
docker exec container_id ls -la /app

# View environment
docker exec container_id env

# Run with environment variable
docker exec -e DEBUG=True container_id python script.py
```

**Flags:**
- `-i` = Interactive (keep stdin open)
- `-t` = Allocate pseudo terminal
- `-e` = Set environment variable
- `-u` = Run as user

**Use cases:**
- Debugging running container
- Running one-off commands
- Checking logs/files
- Restarting services
- Running migrations

---

### Q18: How do you remove Docker containers, images, and volumes?

**Answer:**

**Remove containers:**
```bash
# Stop and remove
docker stop container_id
docker rm container_id

# Force remove
docker rm -f container_id

# Remove all stopped containers
docker container prune -f

# Remove all containers
docker rm $(docker ps -aq)
```

**Remove images:**
```bash
# Remove by ID
docker rmi image_id

# Remove by name
docker rmi myapp:1.0

# Remove all unused images
docker image prune -f

# Remove all images (including used)
docker rmi -f $(docker images -q)
```

**Remove volumes:**
```bash
# List volumes
docker volume ls

# Remove volume
docker volume rm mydata

# Remove unused volumes
docker volume prune -f
```

**Clean everything:**
```bash
# Remove stopped containers, dangling images, unused volumes
docker system prune -f

# Also remove images
docker system prune -a -f
```

---

### Q19: What's the difference between COPY and ADD in Dockerfile?

**Answer:**

| Feature | COPY | ADD |
|---------|------|-----|
| Copy files | ✅ | ✅ |
| Copy dirs | ✅ | ✅ |
| Handle URLs | ❌ | ✅ |
| Auto-extract tar | ❌ | ✅ |
| Recommended | ✅ (usually) | Less common |

**Examples:**

**COPY (preferred):**
```dockerfile
COPY requirements.txt /app/
COPY . /app/
```

**ADD (special cases):**
```dockerfile
# From URL
ADD https://example.com/file.tar.gz /app/

# Auto-extract tar
ADD archive.tar.gz /app/
# Extracts to /app/
```

**Best practice:**
Use COPY unless you specifically need ADD's features (URL fetching, tar extraction).

---

### Q20: What are Docker restart policies?

**Answer:**
Controls how Docker handles container restarts.

**Policies:**

```bash
# No restart (default)
docker run myapp:1.0

# Always restart
docker run --restart=always myapp:1.0

# Restart on failure (max 3 times)
docker run --restart=on-failure:3 myapp:1.0

# Unless stopped
docker run --restart=unless-stopped myapp:1.0
```

**Use cases:**
- `always`: Production services
- `on-failure:N`: Retry N times then stop
- `unless-stopped`: Survive Docker daemon restart

**In docker-compose.yml:**
```yaml
services:
  app:
    restart_policy:
      condition: on-failure
      max_attempts: 3
```

---

## Level: Advanced

### Q21: Explain Docker image layers and caching.

**Answer:**
Each instruction in Dockerfile creates a layer. Docker caches layers for faster builds.

**Example:**
```dockerfile
FROM python:3.9              # Layer 1 (cached from registry)
WORKDIR /app                 # Layer 2 (small, cached)
COPY requirements.txt /app/  # Layer 3 (cached if file unchanged)
RUN pip install -r requirements.txt  # Layer 4 (large, often rebuilt)
COPY . /app                  # Layer 5 (often changes)
CMD ["python", "app.py"]     # Layer 6 (cached)
```

**Caching strategy:**
```dockerfile
# Good: Stable dependencies cached, code frequently changes
FROM python:3.9
WORKDIR /app
COPY requirements.txt /app/          # Cache if stable
RUN pip install -r requirements.txt
COPY . /app                          # Cache if code unchanged
CMD ["python", "app.py"]
```

**Bad: Code change rebuilds everything**
```dockerfile
COPY . /app                          # Everything copied first
RUN pip install -r requirements.txt  # Rebuilt on any file change
```

**View layers:**
```bash
docker history image_id
docker inspect image_id | grep -A10 RootFS
```

---

### Q22: What is a multi-stage Dockerfile build?

**Answer:**
Use multiple FROM statements to create lightweight production images.

**Purpose:**
- Build stage: Includes compiler, dev tools, large dependencies
- Runtime stage: Only what's needed to run

**Example (Python):**
```dockerfile
# Stage 1: Build dependencies
FROM python:3.9 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime (small)
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

**Result:**
- Builder stage: ~1GB (with compiler, build tools)
- Runtime stage: ~200MB (only dependencies)
- Significant size reduction

**Example (Node.js):**
```dockerfile
# Build stage
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Runtime stage
FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
CMD ["node", "app.js"]
```

---

### Q23: How do you debug a Docker container?

**Answer:**
Multiple techniques:

**1. View logs:**
```bash
docker logs -f container_id
docker logs --tail 100 container_id
```

**2. Execute bash:**
```bash
docker exec -it container_id bash
# Then explore: ls, cat, ps, etc.
```

**3. Inspect container:**
```bash
docker inspect container_id
# Check: Status, Mounts, Environment, etc.
```

**4. Check processes:**
```bash
docker top container_id
# See running processes inside
```

**5. Monitor resources:**
```bash
docker stats container_id
# Check CPU, memory, network
```

**6. Copy files out:**
```bash
docker cp container_id:/app/logs/error.log ./
```

**7. Attach to container:**
```bash
docker attach container_id
# See container's stdout/stderr
```

**8. Check exit code:**
```bash
docker inspect container_id | grep ExitCode
```

---

### Q24: Explain Docker security best practices.

**Answer:**

**1. Don't run as root:**
```dockerfile
# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

**2. Keep images small:**
- Fewer components = fewer vulnerabilities
- Use slim/alpine base images

**3. Don't hardcode secrets:**
```dockerfile
# BAD
ENV API_KEY=my_secret_key

# GOOD: Use runtime secrets
docker run -e API_KEY=$API_KEY app:1.0
```

**4. Use specific versions:**
```dockerfile
# Bad (unpredictable)
FROM python:latest

# Good (reproducible)
FROM python:3.9.15-slim-bullseye
```

**5. Scan for vulnerabilities:**
```bash
docker scan myapp:1.0
```

**6. Keep images up-to-date:**
```bash
# Regular base image updates
docker pull python:3.9-slim
docker build -t myapp:1.1 .
```

**7. Use read-only root:**
```bash
docker run --read-only app:1.0
```

**8. Limit resource usage:**
```bash
docker run -m 512m --cpus 0.5 app:1.0
```

---

### Q25: What are the differences between docker run and docker-compose?

**Answer:**

| Aspect | docker run | docker-compose |
|--------|-----------|-----------------|
| Containers | Single | Multiple |
| Configuration | CLI flags | YAML file |
| Networking | Manual setup | Automatic |
| Dependencies | Manual handling | depends_on |
| Volumes | Flags | YAML config |
| Scaling | Create each manually | Scale all |
| Use case | Simple apps, testing | Complex applications |

**docker run:**
```bash
docker run -p 8000:5000 -e DEBUG=True -v data:/app/data myapp:1.0
```

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  app:
    image: myapp:1.0
    ports:
      - "8000:5000"
    environment:
      - DEBUG=True
    volumes:
      - data:/app/data
```

**Usage:**
```bash
docker-compose up -d
```

---

### Q26: How do you handle database connections in Docker?

**Answer:**

**1. Service name as hostname:**
```yaml
# docker-compose.yml
services:
  app:
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
  db:
    image: postgres:13
```

**2. Wait for database:**
```dockerfile
RUN apt-get install -y wait-for-it
```
```yaml
# docker-compose.yml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
```

**3. Python example:**
```python
import os
import psycopg2

db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
```

**4. Connection pooling:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    db_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

---

### Q27: What are Docker resource limits?

**Answer:**
Restrict how much CPU/memory a container uses.

**Command line:**
```bash
# Memory limit
docker run -m 512m app:1.0

# CPU limit
docker run --cpus 0.5 app:1.0

# Memory and CPU
docker run -m 1g --cpus 1 app:1.0
```

**docker-compose.yml:**
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

**Why:**
- Prevent one container from consuming all resources
- Fair resource sharing
- Cost control in cloud
- Predictable performance

---

### Q28: How do you implement CI/CD with Docker?

**Answer:**

**GitHub Actions example:**
```yaml
name: Build and Push Docker Image

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build image
        run: docker build -t ${{ secrets.DOCKER_USERNAME }}/myapp:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push ${{ secrets.DOCKER_USERNAME }}/myapp:${{ github.sha }}
```

**Process:**
1. Developer pushes code
2. CI builds Docker image
3. Tests run in container
4. Image pushed to registry
5. Deploy to production

**Benefits:**
- Consistent build environment
- Automated testing
- Reproducible deployments

---

### Q29: Explain Docker Swarm vs Kubernetes.

**Answer:**

| Aspect | Docker Swarm | Kubernetes |
|--------|-------------|------------|
| Setup | Built-in (docker swarm init) | Complex (many components) |
| Learning curve | Easy | Steep |
| Features | Basic orchestration | Advanced |
| Scalability | Good | Excellent |
| Market adoption | Declining | Industry standard |
| Use case | Small/medium | Enterprise |

**Docker Swarm:**
```bash
# Initialize
docker swarm init

# Deploy service
docker service create --name web -p 8000:5000 myapp:1.0

# Scale
docker service scale web=5
```

**Kubernetes:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: app
    image: myapp:1.0
    ports:
    - containerPort: 5000
```

---

### Q30: What's the difference between ENTRYPOINT and CMD again (Advanced)?

**Answer:**
Deep dive into how they work together.

**Exec form (preferred):**
```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]
```
```bash
docker run myapp:1.0           # python app.py
docker run myapp:1.0 --help    # python --help
docker run myapp:1.0 test.py   # python test.py
```

**Shell form (less common):**
```dockerfile
ENTRYPOINT python app.py
```
- Can't override with args
- Runs in shell (/bin/sh -c)

**Combination:**
```dockerfile
# Best practice
ENTRYPOINT ["python", "-u"]    # -u = unbuffered output
CMD ["app.py"]

# Results in:
# docker run → python -u app.py
# docker run test.py → python -u test.py
```

---

## Bonus: Real-World Scenario Questions

### Q31: How would you containerize a legacy Python application?

**Answer:**
1. Create Dockerfile with same Python version
2. Copy all source code
3. Install dependencies (pip install -r requirements.txt)
4. Set working directory
5. Expose necessary ports
6. Run application
7. Test locally
8. Push to registry

---

### Q32: How do you handle log aggregation with Docker?

**Answer:**
```bash
# JSON logging
docker run --log-driver json-file --log-opt max-size=10m --log-opt max-file=3 app:1.0

# Log to file
docker logs container_id > app.log

# Using ELK stack
# Send logs to Elasticsearch via fluentd or logstash
```

---

### Q33: How do you handle configuration management in Docker?

**Answer:**
```bash
# Environment variables (dev)
docker run -e CONFIG=dev app:1.0

# Config files (mounted)
docker run -v /configs/config.yml:/app/config.yml app:1.0

# Secrets (Docker Swarm/K8s)
docker secret create db_password /path/to/password
```

---

## Interview Preparation Tips

✅ **Understand core concepts:** Image, container, Dockerfile, registry  
✅ **Know common commands:** build, run, push, pull, logs, exec  
✅ **Practice docker-compose:** Multi-container orchestration  
✅ **Explain trade-offs:** Docker vs VM, Docker vs K8s  
✅ **Real-world examples:** ML deployment, web apps, databases  
✅ **Security mindset:** Non-root user, secrets management, scanning  
✅ **Troubleshooting:** Log viewing, exec into container, inspect  
✅ **Performance:** Image size, layer caching, resource limits  

---

**Good luck with your Docker interviews! 🐳**
