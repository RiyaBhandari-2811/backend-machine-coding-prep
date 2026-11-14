# Docker Concepts & Fundamentals

## Table of Contents
1. [What is Docker?](#what-is-docker)
2. [Why Do We Need Docker?](#why-do-we-need-docker)
3. [Core Concepts](#core-concepts)
4. [Dockerfile Basics](#dockerfile-basics)
5. [Docker Workflow](#docker-workflow)
6. [Quick Start](#quick-start)

---

## What is Docker?

### Definition
Docker is a containerization platform that allows you to package your application with all its dependencies into a standardized unit called a **container**. This ensures your application runs the same way everywhere.

### Real-World Analogy
**Traditional Deployment (No Docker):**
```
Your laptop → Works perfectly ✅
Colleague's laptop → "It works on my machine" 😅
Production server → Breaks 💥
```

**With Docker:**
```
Docker container → Works on laptop ✅
Docker container → Same container on colleague's laptop ✅
Docker container → Same container on production server ✅
```

### Why This Matters
Imagine ordering Maggi noodles:
- **Without Docker:** Each person buys noodles separately, adds their own water, salt, spices. Everyone gets different taste.
- **With Docker:** Pre-packaged with exact ingredients. Same taste everywhere.

---

## Why Do We Need Docker?

### Problem 1: Environment Inconsistency
```
Developer: Python 3.9, Django 4.0, PostgreSQL 13
Test Server: Python 3.8, Django 3.2, PostgreSQL 12
Production: Python 3.7, Django 3.1, PostgreSQL 11
Result: Different behavior everywhere 😞
```

**Docker Solution:** Same exact environment everywhere

---

### Problem 2: Dependency Conflicts
```
Project A: Requires numpy==1.19.0
Project B: Requires numpy==1.20.0

Same machine? 
Dependencies conflict 💥
```

**Docker Solution:** Each app in isolated container with its dependencies

---

### Problem 3: Slow Deployment
```
Deploy to production:
1. SSH to server
2. Install Python
3. Install dependencies
4. Copy code
5. Configure database
6. Start application
Time: 30 minutes

Next deploy: Repeat everything 😫
```

**Docker Solution:**
```
docker pull myapp:1.0
docker run -d myapp:1.0
Time: 5 seconds ⚡
```

---

### Problem 4: Infrastructure Overhead
```
5 applications on one server
Each needs its own VM
Each VM: 4GB RAM + 20GB disk
Total: 20GB RAM + 100GB disk

Cost: Very high 💰
Performance: Poor
```

**Docker Solution:**
```
5 applications in containers
Shared OS kernel
Total: 2GB RAM + 10GB disk

Cost: Low 💰
Performance: Great
```

---

## Core Concepts

### 1. Docker Image

**What:** A blueprint or template for creating containers.

**Analogy:** Like a recipe, class definition, or DVD of a movie.

**Characteristics:**
- Static (doesn't change)
- Reusable (one image → multiple containers)
- Layered (built from multiple layers)
- Portable (works anywhere)

**Example:**
```bash
# Pull image from Docker Hub
docker pull python:3.9

# Build your own image
docker build -t myapp:1.0 .
```

**Where do images come from?**
1. **Docker Hub** (official and community images)
2. **Build your own** (using Dockerfile)
3. **Company registry** (private images)

---

### 2. Docker Container

**What:** A running instance of a Docker image.

**Analogy:** Image = Class, Container = Object instance

**Characteristics:**
- Dynamic (has state, can change)
- Temporary (by default, gone when stopped)
- Isolated (processes can't escape)
- Lightweight (shares OS kernel)

**Comparison:**
```
Laptop analogy:
DVD (image) → Movie playing on TV (container)

Software analogy:
Program.exe (image) → Process running (container)

OOP analogy:
class MyClass (image) → obj = MyClass() (container)
```

**Example:**
```bash
# Create and run container
docker run -d -p 8000:5000 myapp:1.0
        └─┬─┘  └──┬──┘
      background  port mapping
      
# List running containers
docker ps
```

---

### 3. Dockerfile

**What:** A text file with instructions to build a Docker image.

**Analogy:** Recipe for cooking, build instructions for a model

**Basic Structure:**
```dockerfile
FROM python:3.9              # Start with base image
WORKDIR /app                 # Set working directory
COPY . /app                  # Copy application code
RUN pip install -r requirements.txt  # Install dependencies
EXPOSE 5000                  # Document which port is used
CMD ["python", "app.py"]     # Command when container starts
```

**Key Instructions:**

| Instruction | Purpose | Example |
|-----------|---------|---------|
| FROM | Base image to start with | FROM python:3.9 |
| WORKDIR | Set working directory | WORKDIR /app |
| COPY | Copy files from host to container | COPY . /app |
| ADD | Copy + can extract tar, download URLs | ADD file.tar.gz /app |
| RUN | Execute command during build | RUN pip install -r requirements.txt |
| ENV | Set environment variable | ENV DEBUG=True |
| EXPOSE | Document port (informational) | EXPOSE 5000 |
| CMD | Default command when container starts | CMD ["python", "app.py"] |
| ENTRYPOINT | Configure container as executable | ENTRYPOINT ["python"] |
| USER | Run as specific user | USER appuser |

---

### 4. Registry

**What:** Storage for Docker images (like GitHub for code)

**Most popular:** Docker Hub (hub.docker.com)

**Examples:**
```bash
# Pull from Docker Hub (official images)
docker pull ubuntu:20.04
docker pull python:3.9
docker pull postgres:13

# Pull from your registry
docker pull username/myapp:1.0

# Private registry
docker pull company-registry.com/internal-app:1.0
```

**Public vs Private:**
- **Public:** Anyone can download
- **Private:** Only authorized users can download

---

### 5. Layer

**What:** Each instruction in Dockerfile creates a layer.

**Visual:**
```
Layer 6: CMD ["python", "app.py"]           ← Top layer (executable)
Layer 5: COPY . /app                         ← Application code
Layer 4: RUN pip install -r requirements.txt ← Dependencies
Layer 3: WORKDIR /app                        ← Directory
Layer 2: RUN apt-get install curl           ← Tools
Layer 1: FROM python:3.9                     ← Base image
```

**Why layers matter:**
- **Caching:** Docker reuses layers if unchanged
- **Size:** Each layer = size added
- **Build speed:** Cached layers skip rebuilding

**Example:**
```dockerfile
# Bad: Changes in layer 3 force rebuilds of layers 3,4,5
COPY . /app
RUN pip install -r requirements.txt
RUN python setup.py

# Good: Only dependencies layer rebuilds when requirements change
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app
RUN python setup.py
```

---

## Dockerfile Basics

### Simple Example: Python Application

```dockerfile
# 1. Start with Python base image
FROM python:3.9-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy requirements file (without code)
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY . .

# 6. Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

# 7. Expose the port the app listens on
EXPOSE 5000

# 8. Health check (optional)
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

# 9. Default command to run
CMD ["python", "app.py"]
```

### Build Process

```bash
# Build the image
docker build -t myapp:1.0 .
           └─┬──┘  └─┬────┘ └─┬─┘
            command  tag     build context
                           (path to Dockerfile)
```

**What happens:**
1. Docker reads Dockerfile
2. Executes FROM instruction (gets base image)
3. Creates layer 1
4. Executes WORKDIR instruction
5. Creates layer 2
6. ... repeats for each instruction
7. Final image = all layers stacked

**Output:**
```
Step 1/9 : FROM python:3.9-slim
 ---> abc123def456
Step 2/9 : WORKDIR /app
 ---> Running in xyz789
 ---> 789xyz456abc
Removing intermediate container xyz789
Step 3/9 : COPY requirements.txt .
 ---> 456abc789xyz
...
Successfully built myapp:1.0
```

---

### Layer Caching Optimization

```dockerfile
# GOOD: Stable layer first (cached longer)
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .           # ← Changed less often
RUN pip install -r requirements.txt
COPY . .                          # ← Changed frequently
CMD ["python", "app.py"]

# Building scenarios:
# Build 1: Everything built (no cache)
# Change app code:
#   - Layers 1-3: Cached (reused)
#   - Layer 4: Fresh build (code changed)
# Build 3: Fast rebuild (reused 3 layers)

# BAD: Everything copied first (cache invalidated)
FROM python:3.9-slim
WORKDIR /app
COPY . .                          # ← Changes often
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

# Building scenarios:
# Change app code:
#   - Layer 1-2: Cached
#   - Layer 3: Fresh build (code changed)
#   - Layer 4: Fresh build (depends on changed layer)
# Build 3: Slower rebuild (only 2 layers cached)
```

---

### Common Dockerfile Patterns

**Pattern 1: Multi-stage build (smaller image)**
```dockerfile
# Build stage
FROM python:3.9 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage (small)
FROM python:3.9-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

**Pattern 2: Non-root user (security)**
```dockerfile
FROM python:3.9-slim
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
USER appuser
CMD ["python", "app.py"]
```

**Pattern 3: Health check (monitoring)**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1
CMD ["python", "app.py"]
```

---

## Docker Workflow

### Step-by-Step Process

**Step 1: Write Dockerfile**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**Step 2: Build Image**
```bash
docker build -t myapp:1.0 .
# Creates: myapp:1.0 image
```

**Step 3: Create Container**
```bash
docker run -d -p 8000:5000 myapp:1.0
# Creates: container from myapp:1.0 image
```

**Step 4: Access Application**
```bash
# Open browser
http://localhost:8000

# Or use curl
curl http://localhost:8000
```

### Workflow Diagram

```
┌─────────────────────────────────────────────────┐
│          DEVELOPMENT                             │
│  1. Write Python application                    │
│  2. Create requirements.txt                     │
│  3. Write Dockerfile                           │
│  4. docker build -t myapp:1.0 .               │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│          IMAGE CREATED                           │
│  myapp:1.0 (blueprint ready)                    │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│          TESTING (local)                         │
│  1. docker run -d -p 8000:5000 myapp:1.0      │
│  2. Test at http://localhost:8000              │
│  3. docker logs container_id                   │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│          REGISTRY (push)                        │
│  1. docker login                                │
│  2. docker tag myapp:1.0 user/myapp:1.0       │
│  3. docker push user/myapp:1.0                 │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│          PRODUCTION (deploy)                    │
│  1. docker pull user/myapp:1.0                 │
│  2. docker run -d -p 8000:5000 user/myapp:1.0 │
│  3. Application running                        │
└─────────────────────────────────────────────────┘
```

---

## Quick Start

### 1. First Container in 30 Seconds

```bash
# Pull and run official hello-world
docker run hello-world

# Output:
# Hello from Docker!
# This message shows that your installation appears to be working correctly.
```

### 2. Run Ubuntu Container

```bash
# Run interactive bash in Ubuntu
docker run -it ubuntu:20.04 bash

# Inside container:
root@container:/# ls
root@container:/# echo "Hello from Docker"
root@container:/# exit
```

### 3. Run Python REPL

```bash
# Interactive Python
docker run -it python:3.9 python

# Inside container:
>>> print("Hello from Docker")
Hello from Docker
>>> exit()
```

### 4. Run Python Script

```bash
# Create script
echo 'print("Hello from Docker")' > script.py

# Run it in container
docker run -v $(pwd):/app python:3.9 python /app/script.py
```

---

## Summary

**Key Takeaways:**

✅ Docker packages app + dependencies in containers  
✅ Image = Blueprint, Container = Running instance  
✅ Dockerfile = Instructions to build image  
✅ Layers = Build steps (enable caching)  
✅ Registry = Image storage (Docker Hub)  
✅ Workflow: Write → Build → Run → Test → Push → Deploy  

**Next Steps:**
→ Read `docker-architecture.md` to understand internals  
→ Read `docker-vs-alternatives.md` to understand trade-offs  
→ Move to Module 2 for practical examples  

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Docker command not found" | Install Docker first (see SETUP.md) |
| "Cannot connect to Docker daemon" | Start Docker daemon (docker desktop or systemctl start docker) |
| "Port already in use" | Use different port: `docker run -p 8001:5000` |
| "Image not found" | Build first: `docker build -t myapp:1.0 .` |
| "Permission denied" | Add to docker group: `usermod -aG docker $USER` |

---

**Ready for practical examples?** → Module 2: Practical Implementation
