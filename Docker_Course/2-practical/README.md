# Module 2: Practical Implementation (50 minutes)

## Overview
This module covers real-world Docker applications with working examples and best practices.

**Time allocation:** 50 minutes  
**Topics:** 12  
**Files:** Multiple working examples + guides

---

## Topics Covered

### 1. Flask Application Container (8 min)
- Containerize a Flask web application
- Multi-layer Dockerfile
- Volume mounting for development
- Environment configuration

**Example:** Simple multiplication table app with HTML UI

**File:** `examples/flask-app/`

---

### 2. Machine Learning Model Deployment (7 min)
- Containerize Streamlit ML app
- Model serving in container
- GPU support basics
- Resource allocation

**Example:** Insurance premium prediction with scikit-learn

**File:** `examples/ml-app/`

---

### 3. Full-Stack Application (10 min)
- Frontend (Flask UI)
- Backend (API)
- Database (PostgreSQL)
- Cache (Redis)
- Multi-container with Compose

**Example:** Complete application stack

**File:** `examples/full-stack/`

---

### 4. Docker Compose Fundamentals (8 min)
- Write docker-compose.yml
- Define multiple services
- Volume management
- Environment variables
- Dependencies between services

**File:** `docker-compose.yml` + `docker-compose-guide.md`

---

### 5. Dockerfile Patterns & Best Practices (8 min)
- Multi-stage builds
- Minimizing image size
- Security best practices
- Caching optimization
- Layer organization

**File:** `DOCKERFILE_PATTERNS.md`

---

### 6. Docker Commands Reference (5 min)
- Complete command reference
- Practical examples
- Debugging techniques
- Common workflows

**File:** `DOCKER_COMMANDS.md`

---

### 7. Health Checks & Monitoring (4 min)
- Adding health checks
- Container monitoring
- Log aggregation
- Performance metrics

**Integrated in examples**

---

## Learning Path

```
1. Start: Flask Application
   Read: flask-app/README.md
   Build: docker build
   Run: docker run
   Test: curl http://localhost:5000
         ↓

2. Intermediate: ML Application
   Read: ml-app/README.md
   Build: Similar to Flask
   Run: docker run with volume mount
   Test: Open browser to Streamlit
         ↓

3. Advanced: Full-Stack with Compose
   Read: full-stack/README.md
   Write: docker-compose.yml
   Run: docker-compose up
   Test: Test all services together
         ↓

4. Reference: Patterns & Commands
   Read: DOCKERFILE_PATTERNS.md
   Read: DOCKER_COMMANDS.md
   Read: docker-compose-guide.md
         ↓

5. Next: Module 3 (Advanced topics)
```

---

## File Structure

```
2-practical/
├── README.md (this file)
├── examples/
│   ├── flask-app/
│   │   ├── README.md
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app.py
│   │   └── templates/
│   │       └── index.html
│   ├── ml-app/
│   │   ├── README.md
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app.py
│   │   └── model.pkl
│   └── full-stack/
│       ├── README.md
│       ├── docker-compose.yml
│       ├── flask-backend/
│       ├── postgres-init/
│       ├── nginx-config/
│       └── .env
├── DOCKERFILE_PATTERNS.md
├── DOCKER_COMMANDS.md
├── docker-compose-guide.md
└── .dockerignore
```

---

## Quick Start (10 min)

### Option 1: Flask Application

```bash
cd examples/flask-app

# Build image
docker build -t flask-app:1.0 .

# Run container
docker run -d -p 5000:5000 --name flask-app flask-app:1.0

# Test
curl http://localhost:5000

# View logs
docker logs -f flask-app

# Stop
docker stop flask-app
docker rm flask-app
```

### Option 2: Multi-Container with Compose

```bash
cd examples/full-stack

# Start all services
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f

# Stop all
docker-compose down
```

---

## Key Concepts

### Docker Compose
- YAML configuration file
- Define all services together
- Automatic networking
- Volume management
- Environment configuration
- Dependency ordering

### Multi-Stage Builds
- Reduce image size
- Build dependencies separate
- Only runtime artifacts in final image
- Better security

### Health Checks
- Verify container is ready
- Docker daemon monitors
- Automatic restart on failure
- Used by orchestration platforms

### Volume Types
- Named volumes (managed by Docker)
- Bind mounts (host directory)
- tmpfs (temporary, memory)

---

## Hands-On Exercises

### Exercise 1: Build Flask App
**Time:** 10 minutes
1. Navigate to `examples/flask-app/`
2. Read Dockerfile
3. Build image: `docker build -t myflask:1.0 .`
4. Run container: `docker run -p 5000:5000 myflask:1.0`
5. Test at http://localhost:5000
6. Modify app.py
7. Rebuild and run
8. Verify changes

**Learning:** Image building, running, testing, iteration

### Exercise 2: Docker Compose
**Time:** 10 minutes
1. Navigate to `examples/full-stack/`
2. Read docker-compose.yml
3. Start services: `docker-compose up -d`
4. List services: `docker-compose ps`
5. View logs: `docker-compose logs flask-backend`
6. Execute command: `docker-compose exec postgres psql -U user`
7. Scale service: `docker-compose up -d --scale worker=3`
8. Stop: `docker-compose down`

**Learning:** Multi-container orchestration, service communication, scaling

### Exercise 3: Modify and Redeploy
**Time:** 10 minutes
1. Edit Flask app code
2. Rebuild image: `docker build -t myflask:2.0 .`
3. Update docker-compose.yml with new image version
4. Deploy: `docker-compose up -d`
5. Verify new version running
6. Rollback: Change version, `docker-compose up -d`

**Learning:** CI/CD workflow, versioning, rolling updates

---

## Key Takeaways

✅ Docker is practical for real applications  
✅ docker-compose simplifies multi-container setup  
✅ Proper Dockerfile structure enables caching  
✅ Health checks ensure reliability  
✅ Volumes persist data across container restarts  
✅ Environment variables enable configuration  

---

## Common Patterns

### Pattern 1: Development Workflow
```bash
# Build
docker build -t app:dev .

# Run with volume mount for live code editing
docker run -v $(pwd):/app app:dev

# Changes reflect immediately (for interpreted languages)
```

### Pattern 2: Production Build
```dockerfile
# Multi-stage
FROM python:3.9 AS builder
# Build dependencies

FROM python:3.9-slim
# Copy artifacts only
```

### Pattern 3: Database with Persistence
```yaml
services:
  db:
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### Pattern 4: Scaling with Compose
```bash
# Scale service to 5 instances
docker-compose up -d --scale worker=5
```

---

## Debugging Tips

### View Container Logs
```bash
docker logs container_id
docker logs -f container_id        # Follow
docker logs --tail 50 container_id # Last 50 lines
```

### Execute Commands in Container
```bash
docker exec -it container_id bash
docker exec container_id python script.py
```

### Check Container Processes
```bash
docker top container_id
docker stats container_id
```

### Inspect Container
```bash
docker inspect container_id
docker inspect -f '{{.NetworkSettings.IPAddress}}' container_id
```

---

## Interview Questions

**Q1: What's the difference between `docker run` and `docker exec`?**
A: run creates a new container; exec executes a command in an already-running container.

**Q2: How do you publish a container's port to the host?**
A: Use `-p host_port:container_port` flag: `docker run -p 8000:5000 my-app`

**Q3: What does `-v` flag do in `docker run`?**
A: Mounts a volume (persistent storage) from host to container.

**Q4: How do you pass environment variables to a container?**
A: Use `-e` flag: `docker run -e VAR_NAME=value my-app`

**Q5: What's the difference between `ENTRYPOINT` and `CMD` in practice?**
A: ENTRYPOINT is the binary; CMD is the default argument (can be overridden at runtime).

**Q6: How do you see a container's file system?**
A: Use `docker exec -it container_id bash` to access the container shell.

**Q7: Can you run multiple commands in a container at startup?**
A: Yes, use a shell script as ENTRYPOINT or string commands with bash -c.

**Q8: What does `docker-compose` solve?**
A: Manages multiple containers as a single application (networks, volumes, dependencies).

**Q9: How do you build and run a Docker app locally?**
A: `docker build -t name:tag .` then `docker run name:tag`

**Q10: What's the difference between `docker logs` and `docker exec`?**
A: logs shows container output; exec runs new commands inside running container.

---

## 🤔 Confusing Questions (Follow-Up Interview Questions)

### Q11: If you mount a volume to a path, does the container's existing files at that path get deleted?

**Answer:**

NO! But they become hidden/inaccessible:

```bash
# Container has /app/data/file.txt (in image)
docker run -v /host/path:/app/data my-app

# Inside container:
# /app/data/file.txt is HIDDEN (replaced by mounted volume)
# But file still exists in image layer, just inaccessible

# Remove volume mount:
docker run my-app  # Original file visible again
```

**This catches developers off-guard!**

---

### Q12: Can you run `docker exec` on a stopped container?

**Answer:**

NO! Container must be running:

```bash
docker exec container_id bash  # ❌ If container stopped
# Error: container stopped

docker start container_id  # Restart first
docker exec container_id bash  # ✅ Now works
```

---

### Q13: If you use `-e` to set environment variable, is it visible in the image?

**Answer:**

NO! Only visible inside the container at runtime:

```bash
docker run -e MY_VAR=secret my-app
# MY_VAR is accessible inside container process

# But the image doesn't store it:
docker run my-app  # MY_VAR not set!

# To persist in image, use ENV in Dockerfile:
# FROM ubuntu
# ENV MY_VAR=secret
```

---

### Q14: What happens if a port is already in use on the host?

**Answer:**

Port mapping fails:

```bash
docker run -p 8000:5000 app1  # ✅ Uses host port 8000
docker run -p 8000:5000 app2  # ❌ FAILS - port 8000 already in use
# Error: Bind for 0.0.0.0:8000 failed: port is already allocated

# Solution: Use different port
docker run -p 8001:5000 app2  # ✅ Uses host port 8001
```

---

### Q15: Can containers communicate with each other?

**Answer:**

YES! If on same network:

```bash
docker run --name db -d postgres
docker run --link db my-app  # Can connect to 'db' hostname
# OR
docker network create mynet
docker run --network mynet --name db postgres
docker run --network mynet my-app  # Can resolve 'db'
```

---

### Q16: If you `docker stop` a container, can you restart it?

**Answer:**

YES! Container persists (not deleted):

```bash
docker run my-app  # Container ABC starts
docker stop ABC  # Container stops but exists

docker ps  # Empty (not running)
docker ps -a  # Shows ABC as Exited

docker start ABC  # ✅ Restart same container
# Same filesystem state as when stopped
```

---

### Q17: What's the difference between `docker rm` and `docker rmi`?

**Answer:**

- **rm:** Remove container
- **rmi:** Remove image

```bash
docker rm container_id  # Delete container
docker rmi image_id  # Delete image

# Once removed, data is gone (no recovery)
```

---

### Q18: Can you mount a file (not directory) with `-v`?

**Answer:**

YES! Mount individual files:

```bash
docker run -v /host/config.txt:/app/config.txt my-app
# Container reads /app/config.txt from host's /host/config.txt

# Useful for:
# - Passing config files
# - Secrets
# - Single file updates
```

---

### Q19: If you modify a volume on host while container is running, does container see it immediately?

**Answer:**

YES! Volumes are real-time shared:

```bash
# Container running with mounted volume
echo "new content" > /host/data.txt

# Inside container (same file):
docker exec container cat /mounted/data.txt
# "new content" (sees change immediately!)
```

---

### Q20: How do you see what ports a container is exposing?

**Answer:**

Use `docker ps` or `docker port`:

```bash
docker ps
# Shows PORTS: 0.0.0.0:8000->5000/tcp

docker port container_id
# Shows: 5000/tcp -> 0.0.0.0:8000

# Also check Dockerfile:
# EXPOSE 5000  (documents port, doesn't actually expose it!)
```

---

## Next Steps

→ Continue to **Module 3: Advanced Topics**

Where you'll learn:
- Docker networking in depth
- Volume management strategies
- Security hardening
- Performance optimization
- Docker Compose advanced features

---

## Resources

- Complete command reference: [DOCKER_COMMANDS.md](DOCKER_COMMANDS.md)
- Dockerfile patterns: [DOCKERFILE_PATTERNS.md](DOCKERFILE_PATTERNS.md)
- Compose guide: [docker-compose-guide.md](docker-compose-guide.md)
- Cheatsheet: See [CHEATSHEET.md](../CHEATSHEET.md)
- Interview Q&A: See [interview-questions.md](../interview-questions.md)

---

**Estimated time to complete:** 50 minutes  
**Recommended approach:** Do all 3 hands-on exercises
