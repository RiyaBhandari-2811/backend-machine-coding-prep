# Docker Course - Complete Interview Questions & Answers

**Total Questions:** 80  
**Difficulty Levels:** Beginner → Expert  
**Estimated Prep Time:** 4-5 hours  
**Last Updated:** November 2026

---

## 📋 Table of Contents

1. [Quick Stats](#quick-stats)
2. [Chapter 1: Fundamentals (20 Qs)](#chapter-1-fundamentals)
3. [Chapter 2: Practical (20 Qs)](#chapter-2-practical)
4. [Chapter 3: Advanced (20 Qs)](#chapter-3-advanced)
5. [Chapter 4: Deployment (20 Qs)](#chapter-4-deployment)
6. [Interview Prep Tips](#interview-prep-tips)
7. [Quick Reference Table](#quick-reference-table)

---

## Quick Stats

| Metric | Value |
|--------|-------|
| **Total Questions** | 80 |
| **Basic Questions (Q1-Q10 per chapter)** | 40 |
| **Advanced Questions (Q11-Q20 per chapter)** | 40 |
| **Practical Examples** | 150+ |
| **Difficulty Range** | Easy → Expert |
| **Categories** | 14 (Images, Containers, Networking, etc.) |

---

# CHAPTER 1: FUNDAMENTALS

## Q1: What is Docker?

**Difficulty:** 🟢 Easy  
**Category:** Overview  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 30 seconds

**Answer:**
Docker is a containerization platform that packages applications and dependencies into isolated units called containers. Containers are lightweight, consistent, and run the same way everywhere - on your laptop, CI/CD pipeline, or production server.

**Code Example:**
```bash
# Run a container from an image
docker run -d --name web nginx

# Container is isolated but shares host kernel
# Lightweight: ~10MB overhead per container vs 2GB+ for VMs
```

**Interview Tip:** Emphasize "same everywhere" - this solves the "works on my machine" problem.

---

## Q2: What's the difference between Docker and a virtual machine?

**Difficulty:** 🟢 Easy  
**Category:** Architecture  
**Expected Answer Length:** 3-4 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
VMs run a full OS with kernel, taking 2GB+ memory each. Containers share the host kernel, taking only 10-50MB each. VMs take minutes to start; containers start in milliseconds. Containers are more lightweight and efficient.

**Comparison:**
```
VMs:
├── Hypervisor
├── OS (2GB+)
├── App
└── Dependencies

Containers:
├── Docker Engine
├── (Shared Kernel)
├── App + Dependencies (10-50MB)
└── More instances possible on same hardware
```

**Interview Tip:** Know the memory/startup time differences by heart.

---

## Q3: What's the difference between a Docker image and a container?

**Difficulty:** 🟡 Medium  
**Category:** Core Concepts  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
An IMAGE is a blueprint/template (immutable). A CONTAINER is a running instance of that image (mutable). One image can create many containers, like a class and its instances.

**Analogy:**
```
Image = Recipe
Container = Cooked meal

Image = Class (immutable blueprint)
Container = Instance (running execution)

Image = CD with software
Container = Running process from that CD
```

**Code Example:**
```bash
docker pull ubuntu  # Pull image
docker run -it ubuntu  # Create + run container from image

# Same image can create multiple containers:
docker run -d --name web1 nginx
docker run -d --name web2 nginx
# Two separate running instances
```

---

## Q4: How do you create a Docker image?

**Difficulty:** 🟡 Medium  
**Category:** Image Creation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Write a Dockerfile with instructions (FROM, RUN, COPY, etc.), then build with `docker build`. Each instruction creates a layer, and all layers stack to form the final image.

**Dockerfile Example:**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**Building:**
```bash
docker build -t myapp:1.0 .
# Creates image with tag myapp:1.0
```

---

## Q5: What's a layer in Docker?

**Difficulty:** 🟡 Medium  
**Category:** Image Architecture  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Each instruction in a Dockerfile creates a layer - a filesystem change. Layers are stacked and cached. If a layer doesn't change, Docker reuses it instead of rebuilding.

**Visualization:**
```
Layer 5: CMD python app.py
Layer 4: COPY . .
Layer 3: RUN pip install -r requirements.txt
Layer 2: COPY requirements.txt .
Layer 1: WORKDIR /app
Layer 0: FROM python:3.11 (base image)
```

**Interview Tip:** Know that layers enable caching and efficiency.

---

## Q6: What does `docker run` do?

**Difficulty:** 🟢 Easy  
**Category:** Container Management  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1 minute

**Answer:**
Creates a new container from an image and runs it. Combines `docker create` and `docker start`. If the image doesn't exist locally, Docker pulls it first.

**Example:**
```bash
docker run -d --name web -p 8080:80 nginx
# -d: Run detached (background)
# --name: Container name
# -p: Port mapping
# nginx: Image name
```

---

## Q7: What's the difference between CMD and ENTRYPOINT in a Dockerfile?

**Difficulty:** 🟡 Medium  
**Category:** Dockerfile  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Both define the default command. ENTRYPOINT is the main executable (shouldn't change). CMD is the default argument (can be overridden). Use ENTRYPOINT for the main process, CMD for default args.

**Example:**
```dockerfile
# ENTRYPOINT - main process
ENTRYPOINT ["python"]

# CMD - default arguments  
CMD ["app.py"]

# Container runs: python app.py
# Can override CMD: docker run image app.py arg1 arg2
# Can't easily override ENTRYPOINT
```

---

## Q8: What does `docker ps` show?

**Difficulty:** 🟢 Easy  
**Category:** Container Management  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 30 seconds

**Answer:**
Lists running containers with details (ID, image, status, ports, names). Use `-a` to see all containers (including stopped ones).

**Example:**
```bash
docker ps          # Running containers
docker ps -a       # All containers (running + stopped)
```

---

## Q9: How do you stop a running container?

**Difficulty:** 🟢 Easy  
**Category:** Container Management  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `docker stop container_name`. It sends SIGTERM signal. If the process doesn't stop, use `docker kill` which sends SIGKILL.

**Example:**
```bash
docker stop mycontainer    # Graceful shutdown (30s timeout)
docker kill mycontainer    # Forceful termination
```

---

## Q10: How do you access a running container's shell?

**Difficulty:** 🟡 Medium  
**Category:** Container Management  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `docker exec -it container_name /bin/bash` to run interactive commands inside a running container.

**Example:**
```bash
docker exec -it myapp /bin/bash
# Now you have a shell inside the container
ls -la
cat /etc/os-release
```

---

## Q11: If you have a parent image with a large base layer, and 100 containers run from it, does each container get 100 copies of that layer?

**Difficulty:** 🟠 Hard  
**Category:** Image Architecture  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
NO! Layers are READ-ONLY and SHARED. The base layer exists once on disk. Each container gets a thin writable layer on top. This is why containers are lightweight.

**Visualization:**
```
Base Layer (10MB, shared) ← 100 containers read from this
├── Container1 Writable Layer (5MB each) ← Each gets its own
├── Container2 Writable Layer (5MB each)
├── ...
└── Container100 Writable Layer (5MB each)

Total disk: 10MB + (100 × 5MB) = 510MB (not 100 × 10MB = 1000MB)
```

**Interview Tip:** This is crucial for understanding container efficiency.

---

## Q12: Can you modify a layer in a running container?

**Difficulty:** 🟡 Medium  
**Category:** Container Runtime  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, you can modify the writable layer, but changes are lost when the container stops. To persist changes, commit them to a new image with `docker commit`.

**Example:**
```bash
docker run -it ubuntu
# Inside container:
touch /newfile.txt
exit

# Changes are lost (container's writable layer is discarded)
# To persist:
docker commit container_id myimage:updated
```

---

## Q13: If you create a multi-line Dockerfile and then modify just one line, what happens when you rebuild?

**Difficulty:** 🟠 Hard  
**Category:** Image Caching  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Docker uses layer caching. If a layer hasn't changed, it reuses the cached layer. Once you modify a line, that layer and ALL subsequent layers rebuild (cache is invalidated).

**Example:**
```dockerfile
# Original
FROM python:3.11          # Layer 0 (cached)
WORKDIR /app              # Layer 1 (cached)
RUN apt-get update        # Layer 2 (cached)
COPY requirements.txt .   # Layer 3 (cached)
RUN pip install -r ...    # Layer 4 (cached)
COPY . .                  # Layer 5 (cached)

# Modified one line:
FROM python:3.11          # Layer 0 (cached)
WORKDIR /app              # Layer 1 (cached)
RUN apt-get update && apt-get install -y curl  # CHANGED!
# Layer 2 rebuilds ↓
COPY requirements.txt .   # Layer 3 rebuilds
RUN pip install -r ...    # Layer 4 rebuilds
COPY . .                  # Layer 5 rebuilds
# All subsequent layers rebuild!
```

**Interview Tip:** Order instructions from least to most-frequently-changed for optimal caching.

---

## Q14: What's the difference between COPY and ADD in Dockerfile?

**Difficulty:** 🟡 Medium  
**Category:** Dockerfile  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Both copy files, but ADD is more powerful - it can extract tar files and handle remote URLs. COPY is simpler and preferred for basic file copying. Best practice: use COPY unless you need ADD's features.

**Example:**
```dockerfile
# COPY - simple, predictable
COPY requirements.txt .

# ADD - can extract archives
ADD app.tar.gz /app

# ADD - can download files
ADD https://example.com/data.zip /data

# Recommendation: Use COPY for predictability, ADD only when needed
```

---

## Q15: What happens if a Dockerfile instruction has an error?

**Difficulty:** 🟢 Easy  
**Category:** Error Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
The build stops immediately, and the image isn't created. Docker reports which instruction failed. The partially-built layers are cached and reused on next build attempts.

**Example:**
```bash
docker build -t app .
# Step 1: FROM ubuntu  # ✅ Success
# Step 2: RUN apt-get install badpackage  # ❌ FAILS
# Error: Dockerfile build failed
# Image not created
```

---

## Q16: What's the Docker registry?

**Difficulty:** 🟡 Medium  
**Category:** Registry  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
A remote server that stores Docker images. Docker Hub is the default free registry. Push images there, pull images from there. Also can run private registries.

**Example:**
```bash
docker push myusername/myapp:1.0  # Upload to Docker Hub
docker pull myusername/myapp:1.0  # Download from Docker Hub
```

---

## Q17: What does `docker build -t myapp:1.0 .` do?

**Difficulty:** 🟡 Medium  
**Category:** Image Building  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Builds a Docker image from the Dockerfile in the current directory, tags it with name `myapp` and version `1.0`. The `.` is the build context (current directory).

**Example:**
```bash
docker build -t myapp:1.0 .
# myapp = image name (repository)
# 1.0 = tag (version)
# . = build context (Dockerfile location)

# Can also push to registry:
docker build -t username/myapp:1.0 .
```

---

## Q18: Can two containers use the same port?

**Difficulty:** 🟡 Medium  
**Category:** Networking  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
NO! Two containers can't listen on the same host port. But they can listen on the same container port if mapped to different host ports.

**Example:**
```bash
docker run -p 8080:80 nginx   # Map host 8080 → container 80
docker run -p 8081:80 nginx   # Map host 8081 → container 80 (different)

# ❌ This fails:
docker run -p 8080:80 nginx
docker run -p 8080:80 apache  # Port 8080 already in use!
```

---

## Q19: What's the difference between `docker start` and `docker run`?

**Difficulty:** 🟡 Medium  
**Category:** Container Lifecycle  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
`docker run` creates a NEW container and starts it. `docker start` starts an EXISTING stopped container. Use `run` for new containers, `start` to restart stopped containers.

**Example:**
```bash
docker run -d --name web nginx      # Creates new container, starts it

docker stop web                     # Stops the container

docker start web                    # Starts the same stopped container
# Keeps the same data, same configuration

# vs. running again:
docker run -d --name web nginx      # Creates ANOTHER new container
```

---

## Q20: If you delete an image, do containers using it stop?

**Difficulty:** 🟡 Medium  
**Category:** Image Management  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
NO! Running containers continue running. You CAN'T delete an image if containers are using it (unless forced with -f). Stopped containers keep the image reference but don't prevent deletion.

**Example:**
```bash
docker rmi myimage
# Error: image is in use by container X

docker rmi -f myimage  # Force delete (not recommended)

# Running containers continue running
# But if container restarts, image is needed
```

---

# CHAPTER 2: PRACTICAL

## Q1: What does port mapping (`-p`) do?

**Difficulty:** 🟢 Easy  
**Category:** Networking  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1 minute

**Answer:**
Maps a host port to a container port. Host port is accessible from outside. Container port is internal. Format: `-p hostPort:containerPort`.

**Example:**
```bash
docker run -p 8080:80 nginx
# Host computer: http://localhost:8080
# Forwards to container port 80 (internal nginx)

docker run -p 3000:3000 -p 8000:80 myapp
# Map multiple ports
```

---

## Q2: What's the difference between `docker run -it` and `docker run -d`?

**Difficulty:** 🟡 Medium  
**Category:** Container Execution  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
`-it` = interactive terminal. Keeps stdin/stdout attached, you see output, can interact. `-d` = detached mode. Runs in background, returns immediately.

**Example:**
```bash
# Interactive
docker run -it ubuntu
# You get a shell prompt, can type commands

# Detached
docker run -d nginx
# Returns to prompt immediately
# Container runs in background
docker logs container_name  # View output later
```

---

## Q3: What is a volume in Docker?

**Difficulty:** 🟡 Medium  
**Category:** Storage  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
A way to persist data outside a container's filesystem. Volumes survive container deletion. Three types: named volumes, bind mounts, and tmpfs.

**Example:**
```bash
# Named volume (Docker manages)
docker run -v mydata:/app/data nginx

# Bind mount (host directory)
docker run -v /host/path:/container/path nginx

# tmpfs (in-memory)
docker run --tmpfs /tmp nginx
```

---

## Q4: What happens if you mount a directory that already has files in the container?

**Difficulty:** 🟠 Hard  
**Category:** Volume Gotchas  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
The existing container files are HIDDEN (shadowed). The mounted directory replaces them. When you unmount, the original files reappear.

**Critical Gotcha:**
```bash
# Container has /app/config/settings.ini inside

docker run -v /host/config:/app/config nginx
# Container now sees /host/config
# Original /app/config/settings.ini is hidden!

# If /host/config is empty:
# Container loses access to settings.ini while mounted
```

**Solution:** Use `docker cp` to transfer files or plan volume structure carefully.

---

## Q5: What's the difference between a named volume and a bind mount?

**Difficulty:** 🟡 Medium  
**Category:** Volumes  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Named volumes are Docker-managed, portable, better for data. Bind mounts map host directories, good for development with live code changes.

**Example:**
```bash
# Named volume (Docker manages)
docker run -v mydata:/app/data nginx
# Data stored in Docker's location
# Portable, backed up easily

# Bind mount (host path)
docker run -v $(pwd):/app nginx
# Maps current directory to container
# Good for development (live file changes)
```

---

## Q6: How do you set environment variables in a container?

**Difficulty:** 🟡 Medium  
**Category:** Configuration  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `-e KEY=value` flag. Can pass multiple. Environment variables are available inside the container.

**Example:**
```bash
docker run -e DATABASE_URL=postgres://... -e DEBUG=true myapp
```

---

## Q7: What does `docker logs` do?

**Difficulty:** 🟢 Easy  
**Category:** Debugging  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Shows the container's stdout/stderr output. Useful for debugging and monitoring. Use `-f` to follow (tail) logs in real-time.

**Example:**
```bash
docker logs mycontainer       # Show all logs
docker logs -f mycontainer    # Follow logs (like tail -f)
docker logs --tail 10 mycontainer  # Last 10 lines
```

---

## Q8: How do you remove a container?

**Difficulty:** 🟢 Easy  
**Category:** Cleanup  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
`docker rm container_name`. Container must be stopped first. Use `-f` to force-remove running containers.

**Example:**
```bash
docker rm mycontainer         # Remove stopped container
docker rm -f mycontainer      # Force-remove running container
docker rm $(docker ps -aq)    # Remove all stopped containers
```

---

## Q9: What is Docker Compose?

**Difficulty:** 🟡 Medium  
**Category:** Orchestration  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
A tool to define and run multiple containers as services in a single file (docker-compose.yml). Each service is a container. Services can communicate and share volumes.

**Example:**
```yaml
# docker-compose.yml
version: '3'
services:
  web:
    image: nginx
    ports:
      - "8080:80"
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: secret
```

```bash
docker-compose up        # Start all services
docker-compose down      # Stop all services
```

---

## Q10: How do services in Docker Compose communicate?

**Difficulty:** 🟡 Medium  
**Category:** Networking  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Services are on the same network and can reach each other by service name. `web` service can connect to `db` service using hostname `db`.

**Example:**
```yaml
services:
  web:
    image: myapp
  db:
    image: postgres
```

**Inside web container:**
```python
# Can connect using service name as hostname
db_connection = psycopg2.connect("host=db user=postgres")
# "db" resolves to the postgres service's IP
```

---

## Q11: If a bind mount is empty on the host, what happens to files in the container's directory?

**Difficulty:** 🟠 Hard  
**Category:** Volume Gotchas  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
They're HIDDEN/SHADOWED. The empty host directory replaces the container files. Once unmounted, the original files reappear.

**Critical Gotcha:**
```bash
# Container has /app with many files
# But host /data is empty

docker run -v /data:/app myapp
# Inside container: /app is now empty!
# All original files are hidden

# When container stops and removes the mount:
# Original files reappear (weren't deleted)

# SOLUTION: Ensure host directory has the files first
```

**Interview Tip:** This is a common production bug.

---

## Q12: Can you have read-only volumes?

**Difficulty:** 🟡 Medium  
**Category:** Volume Permissions  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES! Use `:ro` suffix to make volumes read-only. Container can read but not modify.

**Example:**
```bash
docker run -v mydata:/app/data:ro nginx
# /app/data is read-only inside container

docker run -v /config:/etc/config:ro myapp
# Container can't modify /etc/config
```

---

## Q13: What does `docker-compose up -d` do?

**Difficulty:** 🟡 Medium  
**Category:** Docker Compose  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Starts all services in detached mode (background). Use `docker-compose logs` to see output.

**Example:**
```bash
docker-compose up -d          # Start in background
docker-compose logs -f web    # Follow web service logs
```

---

## Q14: If you change a docker-compose.yml file, what do you do?

**Difficulty:** 🟡 Medium  
**Category:** Docker Compose  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Run `docker-compose down` to stop old services, then `docker-compose up -d` to start new ones. Changes apply immediately.

**Example:**
```bash
docker-compose down     # Stop old services
docker-compose up -d    # Start new services with updated config
```

---

## Q15: How do you pass secrets/passwords safely to containers?

**Difficulty:** 🟡 Medium  
**Category:** Security  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `.env` file with Docker Compose, or `--env-file`. NEVER hardcode secrets. Better: use Docker secrets (in Swarm/Kubernetes) or environment-specific files.

**Example:**
```bash
# .env file
DB_PASSWORD=secret123
API_KEY=sk_123456

# docker-compose.yml
services:
  app:
    env_file: .env
    environment:
      - DB_PASSWORD=${DB_PASSWORD}

docker-compose up  # Loads from .env
```

**Never commit `.env` to git!**

---

## Q16: Can a container access the host network?

**Difficulty:** 🟡 Medium  
**Category:** Networking  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, using `--network host`. Container shares the host's network namespace (same IP, same ports). Use carefully - reduces isolation.

**Example:**
```bash
docker run --network host nginx
# nginx listens on host's port 80
# Not isolated from host networking
```

---

## Q17: What happens if you stop a container that has volumes?

**Difficulty:** 🟡 Medium  
**Category:** Volume Persistence  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Data persists! Volumes exist independently of containers. Stop/remove the container, data remains. Start a new container with the same volume to access data.

**Example:**
```bash
docker run -v mydata:/app/data -d myapp  # Create with volume
# Write data to /app/data

docker stop myapp  # Stop container
# Data still exists in volume

docker run -v mydata:/app/data new-image  # New container, same data
# Can access all previous data
```

---

## Q18: How do you monitor container resource usage?

**Difficulty:** 🟡 Medium  
**Category:** Monitoring  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `docker stats` to see real-time CPU, memory, network, disk usage for running containers.

**Example:**
```bash
docker stats              # All running containers
docker stats mycontainer  # Specific container
docker stats --no-stream  # One-time snapshot
```

---

## Q19: Can you limit container memory and CPU?

**Difficulty:** 🟡 Medium  
**Category:** Resource Limits  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES! Use `--memory` and `--cpus` flags to limit resources. Prevents one container from consuming all host resources.

**Example:**
```bash
docker run --memory 512m --cpus 1 myapp
# Max 512MB memory, 1 CPU core
```

---

## Q20: What's the purpose of a `.dockerignore` file?

**Difficulty:** 🟡 Medium  
**Category:** Build Optimization  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Specifies files/directories to exclude from build context. Like `.gitignore`. Reduces build context size and improves build speed.

**Example:**
```
# .dockerignore
node_modules
.git
.env
*.log
__pycache__

docker build .  # Doesn't include these files in context
```

---

# CHAPTER 3: ADVANCED

## Q1: What's Docker networking?

**Difficulty:** 🟡 Medium  
**Category:** Networking  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Docker creates virtual networks that containers connect to. Containers on the same network can communicate by name. Different network drivers provide different behaviors (bridge, host, overlay, etc.).

**Example:**
```bash
docker network create mynet
docker run -d --network mynet --name web nginx
docker run -d --network mynet --name db postgres

# Inside web: ping db  # Works!
# Containers can communicate by name
```

---

## Q2: What's the difference between bridge and host network?

**Difficulty:** 🟡 Medium  
**Category:** Networking  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Bridge network is isolated (default). Host network shares host's networking, reducing isolation but improving performance. Bridge is safer; host is for specific use cases.

**Example:**
```bash
docker run --network bridge myapp   # Isolated network
docker run --network host myapp     # Shares host network (port 80 = host port 80)
```

---

## Q3: Can containers on different networks communicate?

**Difficulty:** 🟡 Medium  
**Category:** Networking  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
NO! By default, containers on different networks can't communicate. You can connect a container to multiple networks, or use links (deprecated).

**Example:**
```bash
docker network create net1
docker network create net2

docker run --network net1 myapp   # Only on net1
docker run --network net2 myapp   # Only on net2
# Can't communicate!

# Solution: Connect container to multiple networks
docker network connect net2 container1  # Now on both net1 and net2
```

---

## Q4: What are multi-stage builds?

**Difficulty:** 🟠 Hard  
**Category:** Build Optimization  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Use multiple FROM statements in Dockerfile. Build in one stage, copy artifacts to final stage. Reduces final image size (no build tools in production).

**Example:**
```dockerfile
# Stage 1: Build
FROM node:16 AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

# Stage 2: Production (small image)
FROM node:16-alpine
COPY --from=builder /app/dist .
CMD ["node", "server.js"]

# Final image: Only production code, no build tools
```

---

## Q5: How do you mount multiple volumes in a container?

**Difficulty:** 🟡 Medium  
**Category:** Volumes  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use multiple `-v` flags. Each volume is mounted independently.

**Example:**
```bash
docker run \
  -v mydata:/app/data \
  -v logs:/app/logs \
  -v /config:/etc/config \
  myapp
```

---

## Q11: If you have a large image and want to reduce its size, what strategies would you use?

**Difficulty:** 🟠 Hard  
**Category:** Image Optimization  
**Expected Answer Length:** 3-4 sentences  
**Time to Answer:** 3 minutes

**Answer:**
1. Use multi-stage builds - build in one stage, copy artifacts to smaller base image  
2. Use smaller base images (alpine instead of ubuntu)  
3. Remove unnecessary files after installation  
4. Use BuildKit for better caching  
5. Chain RUN commands to reduce layers

**Example:**
```dockerfile
# ❌ BLOATED - 1000MB
FROM ubuntu
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python3
COPY . /app

# ✅ OPTIMIZED - 50MB
FROM python:3.11-alpine
RUN apk add --no-cache build-base
COPY . /app
RUN rm -rf /tmp/* /var/cache/apk/*
```

---

## Q12: What's Docker BuildKit?

**Difficulty:** 🟠 Hard  
**Category:** Build Optimization  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
An improved build engine with better caching, parallelization, and additional features. Faster builds. Enable with `DOCKER_BUILDKIT=1`.

**Example:**
```bash
DOCKER_BUILDKIT=1 docker build -t myapp .
# Builds layers in parallel
# Better caching
# Faster overall build time
```

---

## Q13: Can you use wildcards in COPY/ADD Dockerfile commands?

**Difficulty:** 🟡 Medium  
**Category:** Dockerfile  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES! Use glob patterns like `COPY *.py /app/`.

**Example:**
```dockerfile
COPY *.py /app/
COPY src/* /app/src/
ADD config/** /etc/config/
```

---

## Q14: What's a health check in Docker?

**Difficulty:** 🟡 Medium  
**Category:** Container Management  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
A command that runs periodically to verify the container is healthy. If fails, container is marked "unhealthy". Used for orchestration and monitoring.

**Example:**
```dockerfile
FROM nginx
HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost/ || exit 1
```

**Docker Compose:**
```yaml
services:
  web:
    image: myapp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000"]
      interval: 30s
      timeout: 10s
```

---

## Q15: What does `docker inspect` show?

**Difficulty:** 🟡 Medium  
**Category:** Debugging  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Detailed JSON info about a container or image: network settings, volumes, environment, ports, etc. Useful for debugging.

**Example:**
```bash
docker inspect mycontainer     # Get all details
docker inspect mycontainer --format='{{.NetworkSettings.IPAddress}}'  # Specific field
```

---

## Q16: Can you push an image to a private registry?

**Difficulty:** 🟡 Medium  
**Category:** Registry  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES! Tag image with registry address, then push. Need permissions/credentials for private registries.

**Example:**
```bash
docker tag myapp:1.0 registry.example.com/myapp:1.0
docker push registry.example.com/myapp:1.0

# Login first if needed
docker login registry.example.com
```

---

## Q17: What's the difference between `CMD` and `RUN`?

**Difficulty:** 🟡 Medium  
**Category:** Dockerfile  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
RUN executes during BUILD (creates layers). CMD specifies default command to RUN at container start (doesn't create layer, can be overridden).

**Example:**
```dockerfile
RUN apt-get install curl    # Builds an image layer
CMD ["node", "app.js"]      # Runs when container starts

# Build creates image (RUN happens)
# Container starts (CMD happens)
```

---

## Q18: Can you run multiple commands in a single RUN instruction?

**Difficulty:** 🟡 Medium  
**Category:** Dockerfile  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES! Use `&&` or `;` to chain commands. Reduces layers for better caching and smaller images.

**Example:**
```dockerfile
# ✅ Better - One layer
RUN apt-get update && apt-get install -y curl && rm -rf /var/cache

# ❌ Inefficient - Three layers
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/cache
```

---

## Q19: What's the difference between ARG and ENV in Dockerfile?

**Difficulty:** 🟡 Medium  
**Category:** Dockerfile  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
ARG is only available during BUILD. ENV is available at BUILD and RUNTIME. Use ARG for build-time options, ENV for runtime configuration.

**Example:**
```dockerfile
ARG VERSION=1.0          # Available during build only
ENV DATABASE_URL=prod    # Available at runtime

RUN echo $VERSION        # Can use ARG during build
CMD echo $DATABASE_URL   # Can use ENV at runtime
```

---

## Q20: Can you override ENV variables when running a container?

**Difficulty:** 🟡 Medium  
**Category:** Configuration  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES! Use `-e` flag to override ENV variables defined in Dockerfile.

**Example:**
```dockerfile
ENV DEBUG=false
```

```bash
docker run -e DEBUG=true myapp  # Override to true
```

---

# CHAPTER 4: DEPLOYMENT

## Q1: What's the difference between development and production images?

**Difficulty:** 🟡 Medium  
**Category:** Deployment  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Development images include debugging tools, logs, and maybe debug code. Production images are minimal - only what's needed to run the app safely. Production images are smaller, faster, more secure.

**Example:**
```dockerfile
# Development
FROM python:3.11
RUN pip install pytest black pylint  # Dev tools
RUN pip install -r requirements.txt
COPY . /app

# Production (multi-stage)
FROM python:3.11-alpine
RUN pip install -r requirements.txt --no-cache-dir  # Only runtime deps
COPY --from=builder /app/dist /app
```

---

## Q2: What's the difference between Docker and Kubernetes?

**Difficulty:** 🟠 Hard  
**Category:** Orchestration  
**Expected Answer Length:** 3-4 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Docker runs containers on a single machine. Kubernetes orchestrates containers across multiple machines (cluster). Docker is for local development/simple deployments. Kubernetes scales, balances, and manages production workloads.

**Analogy:**
```
Docker = Running programs
Kubernetes = Managing thousands of programs across many computers
```

---

## Q3: How do you scale applications with Docker?

**Difficulty:** 🟡 Medium  
**Category:** Scaling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Run multiple containers. Use load balancer (Nginx, HAProxy) to distribute traffic. Docker Compose or Kubernetes manages this automatically.

**Example:**
```bash
# Run 3 instances
docker run -p 8081:8000 myapp
docker run -p 8082:8000 myapp
docker run -p 8083:8000 myapp

# Nginx load balancer routes traffic
upstream backend {
    server localhost:8081;
    server localhost:8082;
    server localhost:8083;
}
```

---

## Q4: What's AWS ECS?

**Difficulty:** 🟡 Medium  
**Category:** Cloud Deployment  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
AWS Elastic Container Service. AWS's container orchestration platform. Manages Docker containers on EC2 or Fargate (serverless). Alternative to Kubernetes.

**Key Concepts:**
- Task Definition = Docker image + config
- Service = Running tasks
- Cluster = EC2 instances or Fargate

---

## Q5: What's the difference between EC2 and Fargate in ECS?

**Difficulty:** 🟡 Medium  
**Category:** AWS ECS  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
EC2 = You manage servers (patch, monitor, scale). Fargate = AWS manages servers, you just upload containers. Fargate is easier but more expensive. EC2 is cheaper but requires management.

---

## Q11: How do you implement blue-green deployments with Docker?

**Difficulty:** 🟠 Hard  
**Category:** Deployment Strategy  
**Expected Answer Length:** 3-4 sentences  
**Time to Answer:** 2.5 minutes

**Answer:**
Run two production environments (Blue = current, Green = new). Route traffic to Blue. Deploy new code to Green. Test Green thoroughly. Switch traffic to Green. If issues, switch back to Blue.

**Process:**
```
1. Blue production (v1.0) serving traffic
2. Green production (v1.1) deployed, no traffic
3. Test Green thoroughly
4. Switch load balancer to Green
5. If problems, switch back to Blue
6. Old Blue can be cleaned up
```

**Advantages:**
- Zero downtime deployment
- Easy rollback
- Full testing before switching traffic

---

## Q12: What are StatefulSets vs Deployments in Kubernetes?

**Difficulty:** 🟠 Hard  
**Category:** Kubernetes  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Deployments = for stateless apps (web servers). Replicas are interchangeable. StatefulSets = for stateful apps (databases). Each replica has a stable identity and persistent storage.

**Example:**
```
Deployment: web1, web2, web3 (can kill any)
StatefulSet: db-0, db-1, db-2 (each different, ordered startup/shutdown)
```

---

## Q13: How do you handle database migrations during deployment?

**Difficulty:** 🟠 Hard  
**Category:** Deployment Strategy  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Separate migration step from app deployment. Run migrations BEFORE deploying new app code. Or use backward-compatible migrations (add column with default, remove in separate release).

**Strategies:**
```
1. Pre-deployment: Run migrations, then deploy app
2. Backward-compatible: Only add new fields, old app still works
3. Separate migration job: Init container in Kubernetes
```

---

## Q14: What's a Docker registry and why use it?

**Difficulty:** 🟡 Medium  
**Category:** Registry  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Central repository for Docker images. Pull/push images. Docker Hub is public/free. Private registries for sensitive images. Essential for CI/CD pipelines.

**Examples:**
```bash
docker push myrepo/myapp:1.0     # Push to registry
docker pull myrepo/myapp:1.0     # Pull from registry

# Kubernetes pulls from registry automatically
```

---

## Q15: How do you handle secrets in production Docker deployments?

**Difficulty:** 🟡 Medium  
**Category:** Security  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
NEVER hardcode secrets. Use external secret management: Docker Secrets (Swarm), Kubernetes Secrets, or AWS Secrets Manager, HashiCorp Vault.

**Examples:**
```bash
# Docker Secrets
docker secret create db_password secret.txt
docker service create --secret db_password myapp

# Kubernetes
kubectl create secret generic db-secret --from-literal=password=123
kubectl apply -f deployment.yaml  # References secret

# AWS
aws secretsmanager get-secret-value --secret-id db_password
```

---

## Q16: How do you implement CI/CD with Docker?

**Difficulty:** 🟠 Hard  
**Category:** CI/CD  
**Expected Answer Length:** 3-4 sentences  
**Time to Answer:** 2.5 minutes

**Answer:**
1. Developer commits code to Git
2. CI (GitHub Actions, Jenkins) triggers
3. Build Docker image
4. Run tests in container
5. If pass, push image to registry
6. CD system pulls image and deploys

**Pipeline Example:**
```yaml
# GitHub Actions
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Run tests
        run: docker run myapp:${{ github.sha }} npm test
      - name: Push to registry
        run: docker push myapp:${{ github.sha }}
```

---

## Q17: What's container orchestration?

**Difficulty:** 🟡 Medium  
**Category:** Orchestration  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Automated management of containers: scheduling, resource allocation, networking, rolling updates, health checks, scaling. Kubernetes is the most popular.

**Tasks Orchestration Handles:**
- Schedule containers on nodes
- Restart failed containers
- Scale up/down on demand
- Update containers without downtime
- Network services
- Load balancing

---

## Q18: What's a Dockerfile best practice for security?

**Difficulty:** 🟡 Medium  
**Category:** Security  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
1. Don't run as root (use USER)  
2. Use minimal base images (alpine)  
3. Don't hardcode secrets  
4. Scan images for vulnerabilities  
5. Update base images regularly

**Example:**
```dockerfile
FROM python:3.11-alpine
RUN useradd -m appuser
COPY --chown=appuser:appuser . /app
USER appuser
CMD ["python", "app.py"]
```

---

## Q19: How do you implement auto-scaling with containers?

**Difficulty:** 🟠 Hard  
**Category:** Scaling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Monitor CPU/memory metrics. When threshold exceeded, automatically start more container instances. Load balancer distributes traffic. When metrics drop, scale down.

**Kubernetes Example:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-scaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Q20: What's a rolling update?

**Difficulty:** 🟡 Medium  
**Category:** Deployment Strategy  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Gradually replace old containers with new ones (e.g., replace 1 at a time). Maintains zero downtime. Existing instances continue serving traffic while new ones are tested.

**Process:**
```
Deployment: 3 containers v1.0

Rolling Update (1 at a time):
1. Start 1x v1.1 container
2. Remove 1x v1.0 container
3. Start 1x v1.1 container
4. Remove 1x v1.0 container
5. Start 1x v1.1 container
6. Remove last v1.0 container

Result: 3 containers v1.1, zero downtime!
```

---

# Interview Prep Tips

## Key Concepts to Master

1. **Images vs Containers** - Blueprint vs Instance
2. **Layers** - Understanding caching and efficiency
3. **Networking** - How containers communicate
4. **Volumes** - Data persistence and shadowing gotchas
5. **Orchestration** - Scaling and management

## Common Mistakes

- ❌ Confusing images and containers
- ❌ Not understanding layer caching
- ❌ Not knowing volume mounting hides files
- ❌ Hardcoding secrets in Dockerfiles
- ❌ Using large base images
- ❌ Not understanding port mapping

## Study Tips

✅ Run all examples locally  
✅ Modify examples and predict behavior  
✅ Build real multi-container projects  
✅ Understand WHY commands work  
✅ Learn Docker Compose early  
✅ Practice deployment scenarios  

---

# Quick Reference Table

| Concept | Easy Qs | Medium Qs | Hard Qs |
|---------|---------|----------|---------|
| **Fundamentals** | Q1-Q5 | Q6-Q10 | Q11-Q15 |
| **Practical** | Q1-Q5 | Q6-Q10 | Q11-Q15 |
| **Advanced** | Q1-Q5 | Q6-Q10 | Q11-Q15 |
| **Deployment** | Q1-Q5 | Q6-Q10 | Q11-Q15 |

---

**Good luck with your Docker interviews!** 🐳  
Master these concepts and you'll handle any Docker deployment question.
