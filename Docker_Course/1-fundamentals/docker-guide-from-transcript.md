# Chapter 8: Docker - Container Fundamentals & Deployment

## Overview

Learn Docker from fundamentals to production deployment. This chapter covers everything you need to containerize applications, from basic concepts to pushing images to registry and deploying them. Based on practical ML and web application examples.

**Universal Topic:** Required across all roles - Data Scientists, ML Engineers, Backend Developers, DevOps, Frontend Developers

---

## 📚 Table of Contents

1. [What is Docker & Why We Need It](#what-is-docker)
2. [Docker Architecture & Components](#docker-architecture)
3. [Docker Engine Deep Dive](#docker-engine)
4. [Docker Images](#docker-images)
5. [Dockerfile](#dockerfile)
6. [Docker Containers](#docker-containers)
7. [Docker Registry](#docker-registry)
8. [Docker Workflow](#docker-workflow)
9. [Practical Implementation](#practical-implementation)
10. [Interview Questions](#interview-questions)

---

## What is Docker?

### Definition
Docker is a platform designed to help developers **build, share, and run containerized applications**.

### Real-World Analogy: Maggi Noodles

Think of Maggi noodles:
- **Before Docker (Problem):** If Maggi gave you just the recipe and ingredients list, different people using different ingredients would get different taste. Quality inconsistency everywhere.
- **After Docker (Solution):** Maggi pre-packages everything (noodles + seasoning) in a standardized packet. Same taste everywhere - whether in mountains or cities.

**Software Parallel:**
- **Before Docker:** Code works on my machine → Doesn't work on tester's machine (different OS, library versions, dependencies)
- **After Docker:** Containerize application with ALL dependencies → Works everywhere identically

---

## Why Do We Need Docker?

### Reason #1: Consistency Across Environments

**Problem:**
- Applications behave differently in development, testing, and production
- Due to variations in OS, configuration, dependencies, and infrastructure

**Solution:**
- Docker containers encapsulate everything needed to run an application
- Package and distribute the complete "box"
- Result: Consistent behavior across all environments

**Real Scenario:**
1. Developer creates Laptop Price Predictor on their machine
2. Works perfectly locally ✅
3. Pushes code to GitHub
4. Tester downloads and tries to run
5. Error: `ColumnTransformer object has no attribute 'named_transformers'`
6. Root cause: Scikit-learn version mismatch
7. Problem repeats with other libraries...
8. **Solution:** Docker packages entire environment → Tester runs same environment → No version conflicts

### Reason #2: Isolation

**Problem:**
- One server often hosts multiple applications
- If App A is hacked → App B compromised
- If App A needs more resources → App B starved

**Solution:**
- Docker provides isolation between containers on same machine
- Lightweight compared to virtual machines (VMs)
- Fast startup/shutdown

### Reason #3: Scalability

**Problem:**
- Afternoon: Low traffic → Need 3 servers
- Evening: High traffic → Need 5 servers
- Early morning: Traffic drops → Need 3 servers again

**Solution:**
- Since everything is containerized (lightweight)
- Scale up: Start new containers on additional machines instantly
- Scale down: Stop containers when load decreases
- Kubernetes orchestrates this automatically

### Other Use Cases
- Microservices Architecture
- CI/CD Pipelines
- Cloud Migration
- Testing & QA
- Machine Learning Deployment
- API Development

---

## Docker Architecture & Components

### Visual Workflow

```
┌─────────────────────────────────────────────────┐
│             Developer's Machine                  │
│  ┌──────────────────────────────────────────┐   │
│  │  1. Write Dockerfile                      │   │
│  │  2. docker build → Docker Image           │   │
│  │  3. docker run → Docker Container         │   │
│  │  4. Test locally                          │   │
│  └──────────────────────────────────────────┘   │
│                      ↓                           │
│  ┌──────────────────────────────────────────┐   │
│  │  5. docker push → Docker Registry        │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
                       ↓
            ┌──────────────────────┐
            │   Docker Hub/ECR      │
            │   (Public/Private)    │
            └──────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│            Tester's Machine                      │
│  ┌──────────────────────────────────────────┐   │
│  │  6. docker pull → Download Image         │   │
│  │  7. docker run → Execute Container       │   │
│  │  8. Test on their machine                │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## Docker Engine

### Definition
The core component responsible for creating, running, and managing Docker containers.

### Architecture: 3-Layer Model

```
┌─────────────────────────────────────┐
│     Layer 3: User Interface (CLI)   │
│  docker run, docker build, docker ps│
│         (What users interact with)   │
└────────────────┬────────────────────┘
                 │
         ┌───────▼────────┐
         │   REST API     │
         │  (Communication)
         └───────┬────────┘
                 │
┌────────────────▼────────────────────┐
│  Layer 1: Docker Daemon (Server)    │
│   - Creates containers              │
│   - Manages images                  │
│   - Manages networks & volumes      │
│  (Background service on your machine)
└─────────────────────────────────────┘
```

### Components

| Component | Purpose |
|-----------|---------|
| **Docker Daemon** | Background service managing containers, images, networks, volumes |
| **Docker CLI** | Command-line interface for user commands |
| **REST API** | Enables programmatic interaction with Docker |

### Key Point
Docker Daemon runs on **every machine** that needs to execute containers. Installing Docker Desktop gives you all three layers.

---

## Docker Images

### Definition
A lightweight, standalone, executable software package containing:
- Base OS layer
- Application code
- Runtime
- All dependencies
- Configuration files
- Environment variables

### Image Properties
- **Lightweight:** Megabytes to few GB
- **Standalone:** No additional software needed
- **Executable:** Can run immediately
- **Reusable:** Can create multiple containers from one image

### Image Lifecycle: 4 Stages

```
1. CREATION
   └─> docker build → Create image from Dockerfile

2. STORAGE
   └─> Store in local registry (your machine)

3. DISTRIBUTION
   └─> docker push → Upload to Docker Hub/ECR
   └─> Others can docker pull

4. EXECUTION
   └─> docker run → Create container (instance)
```

### What's Inside an Image?

**Layers (stacked):**

```
┌─────────────────────────────────┐
│  Layer 5: Your Code             │
│  (app.py, requirements.txt, etc) │
├─────────────────────────────────┤
│  Layer 4: Configuration         │
│  (ports, env vars, commands)     │
├─────────────────────────────────┤
│  Layer 3: Dependencies           │
│  (Flask, pandas, scikit-learn)   │
├─────────────────────────────────┤
│  Layer 2: Runtime               │
│  (Python 3.9, Node.js, etc)     │
├─────────────────────────────────┤
│  Layer 1: Base OS                │
│  (Alpine, Ubuntu, Debian)        │
└─────────────────────────────────┘
```

Each layer is immutable and cacheable (faster builds on second attempt).

---

## Dockerfile

### Definition
Text file containing instructions to build a Docker image.

### Basic Structure

```dockerfile
# 1. Start with base image
FROM python:3.9

# 2. Set working directory
WORKDIR /app

# 3. Copy files from your machine to container
COPY . /app

# 4. Install dependencies
RUN pip install -r requirements.txt

# 5. Expose port (let container listen on this port)
EXPOSE 5000

# 6. Command to run when container starts
CMD ["python", "app.py"]
```

### Key Instructions

| Instruction | Purpose | Example |
|-------------|---------|---------|
| **FROM** | Base image to start with | `FROM python:3.9` |
| **WORKDIR** | Set working directory inside container | `WORKDIR /app` |
| **COPY** | Copy files from host to container | `COPY . /app` |
| **ADD** | Similar to COPY but can handle URLs | `ADD file.txt /app/` |
| **RUN** | Execute command during build | `RUN pip install -r requirements.txt` |
| **ENV** | Set environment variables | `ENV DEBUG=True` |
| **EXPOSE** | Document which port app listens on | `EXPOSE 5000` |
| **CMD** | Default command when container starts | `CMD ["python", "app.py"]` |
| **ENTRYPOINT** | Configure container as executable | `ENTRYPOINT ["python", "app.py"]` |

### How Build Works

```
Dockerfile
    ↓
docker build
    ↓
Step 1: FROM python:3.9 → Layer 1
Step 2: WORKDIR /app → Layer 2
Step 3: COPY . /app → Layer 3
Step 4: RUN pip install → Layer 4 (caches dependencies)
Step 5: EXPOSE 5000 → Layer 5
Step 6: CMD python app.py → Layer 6
    ↓
Image Created ✅
```

Each step creates a layer. Layers are cached for faster rebuilds.

---

## Docker Containers

### Definition
A running instance of a Docker image - a lightweight, isolated, portable environment that:
- Encapsulates an application
- Contains all its dependencies
- Runs consistently across environments

### Image vs Container Analogy

| Concept | Analogy |
|---------|---------|
| **Image** | DVD of a movie |
| **Container** | Movie playing on your TV |

Same DVD (image) can play on multiple TVs (containers) simultaneously, each with independent state.

### Container Lifecycle

```
┌──────────┐
│  Create  │ ← docker run
└────┬─────┘
     ↓
┌──────────┐
│  Start   │ ← Executing
└────┬─────┘
     ↓
┌──────────┐
│ Running  │ ← docker ps (shows running containers)
└────┬─────┘
     ↓
┌──────────┐
│  Pause   │ ← docker pause
└────┬─────┘
     ↓
┌──────────┐
│  Resume  │ ← docker unpause
└────┬─────┘
     ↓
┌──────────┐
│  Stop    │ ← docker stop
└────┬─────┘
     ↓
┌──────────┐
│  Remove  │ ← docker rm
└──────────┘
```

---

## Docker Registry

### Definition
A service that stores and distributes Docker images. Think of it as GitHub for Docker images.

### Types of Registries

| Type | Example | Visibility | Who Uses |
|------|---------|-----------|----------|
| **Public** | Docker Hub | Anyone can access | Developers, Open Source |
| **Private** | Docker Hub Premium, ECR | Only organization members | Companies |
| **Third-party** | AWS ECR, Google GCR, Azure ACR | Cloud provider specific | Enterprise |

### Docker Hub: Most Popular Public Registry

```
Docker Hub (hub.docker.com)
    ↓
┌─────────────────────────────┐
│ Repositories                 │
│ ├─ tensorflow (1000+ tags)  │
│ ├─ python (500+ tags)       │
│ ├─ node (400+ tags)         │
│ ├─ ubuntu (300+ tags)       │
│ └─ nitishcps/laptop (5 tags)│
└─────────────────────────────┘
```

### Repository Structure

Each repository contains multiple **tags** (versions):

```
tensorflow
├─ 2.12-cpu
├─ 2.12-gpu
├─ 2.11-cpu
├─ latest (points to newest)
└─ ...
```

### Registry Operations

```
YOUR CODE
    ↓
docker build → Image
    ↓
docker push → Upload to Registry
    ↓
REGISTRY (Docker Hub)
    ↓
docker pull ← Download from Registry
    ↓
TESTER'S MACHINE
    ↓
docker run → Container
```

---

## Docker Workflow: Complete Picture

### Step-by-Step Developer → Registry → Tester

```
DEVELOPER'S MACHINE
┌────────────────────────────────┐
│ 1. Write Dockerfile            │
│ 2. Write application code      │
│ 3. Create requirements.txt     │
└────────────┬───────────────────┘
             ↓
┌────────────────────────────────┐
│ 4. docker build -t username/  │
│    appname:tag .               │
└────────────┬───────────────────┘
             ↓
┌────────────────────────────────┐
│ 5. docker run (Test locally)   │
│    ✅ Works correctly           │
└────────────┬───────────────────┘
             ↓
┌────────────────────────────────┐
│ 6. docker push username/       │
│    appname:tag                 │
│    (Upload to registry)        │
└────────────┬───────────────────┘
             ↓
      DOCKER REGISTRY
    (Docker Hub/ECR/GCR)
    Image stored with tags
             ↓
┌────────────────────────────────┐
│ TESTER'S MACHINE               │
│ 7. docker pull username/       │
│    appname:tag                 │
│    (Download image)            │
│ ✅ Image now on tester's       │
│    machine                     │
└────────────┬───────────────────┘
             ↓
┌────────────────────────────────┐
│ 8. docker run -p               │
│    8000:5000 username/appname  │
│    (Run container)             │
│ ✅ Works identically to        │
│    developer's machine!        │
└────────────────────────────────┘
```

### Key Insight
✅ **No more "works on my machine" problem!**

---

## Practical Implementation

### Prerequisites
1. Install Docker Desktop (includes Docker Engine + CLI + GUI)
2. Create Docker Hub account
3. Verify installation: `docker --version`

### Example 1: Flask Application

**Structure:**
```
flask-app/
├── app.py
├── requirements.txt
├── Dockerfile
└── README.md
```

**Dockerfile:**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

**Build:**
```bash
docker build -t yourusername/flask-app:1.0 .
```

**Run:**
```bash
docker run -p 8000:5000 yourusername/flask-app:1.0
```

**Push:**
```bash
docker login  # Authenticate with Docker Hub
docker push yourusername/flask-app:1.0
```

### Example 2: Machine Learning Application

**Common Use Case:** Predict laptop price using Scikit-learn model

**Dockerfile:**
```dockerfile
FROM python:3.7
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

**Build & Push:**
```bash
docker build -t yourusername/laptop-predictor:1.0 .
docker push yourusername/laptop-predictor:1.0
```

**Run from Registry:**
```bash
docker pull yourusername/laptop-predictor:1.0
docker run -p 8501:8501 yourusername/laptop-predictor:1.0
```

---

## Important Concepts

### Port Mapping (-p flag)

```
docker run -p 8000:5000 app-name
           └─────┬────┘└─┬─┘
            host port  container port
```

- `8000` = Port on your machine (what you access)
- `5000` = Port inside container (where app listens)
- Why needed: Your machine might already use 5000, so map to different port

### Detach Mode (-d flag)

```bash
docker run -d -p 8000:5000 app-name  # Runs in background
docker ps  # See running containers
docker logs container_id  # View output
```

### Environment Variables

```dockerfile
ENV DEBUG=True
ENV API_KEY=secret_key
```

Or pass at runtime:
```bash
docker run -e DEBUG=True app-name
```

---

## Interview Questions

**Q1: What's the difference between an image and container?**
A: Image is a template/blueprint (like a DVD). Container is a running instance (like playing the DVD on your TV).

**Q2: Why do we need Docker?**
A: Ensures consistency across dev/test/prod environments. Provides isolation, scalability, and solves "works on my machine" problem.

**Q3: What's a Dockerfile?**
A: Text file with instructions to build an image. Each instruction creates a layer in the image.

**Q4: Explain port mapping.**
A: Maps container port (internal) to host port (your machine). Example: `-p 8000:5000` means access app on http://localhost:8000 even though it runs on port 5000 inside container.

**Q5: What's Docker Hub?**
A: Public registry where developers store and share Docker images. Anyone can pull images; you can push your own.

**Q6: How does versioning work with images?**
A: Using tags. Same codebase can have `v1.0`, `v2.0`, `latest` tags. Pull specific version: `docker pull app:v1.0`

**Q7: What happens if you docker run the same image twice?**
A: Two separate containers are created. They run independently. Stopping one doesn't affect the other.

**Q8: Why use Docker instead of Virtual Machines?**
A: Docker containers are lightweight (no full OS), start instantly, use less resources. VMs are heavier with full OS + kernel.

**Q9: Can I run multiple versions of same app?**
A: Yes! Docker containers are isolated. Run v1.0 on port 8000 and v2.0 on port 8001 simultaneously.

**Q10: What's the best base image for Python ML apps?**
A: `python:3.8` or `python:3.9` (pre-built, includes pip). For lightweight: `python:3.9-slim` or `python:3.9-alpine`.

---

## Best Practices

✅ **Keep images small:** Use slim base images, remove unnecessary dependencies
✅ **Use .dockerignore:** Exclude unnecessary files (like .git, node_modules)
✅ **Pin versions:** Use specific versions (`python:3.9`), not `latest`
✅ **One concern per container:** Avoid monolithic containers (microservices principle)
✅ **Use multi-stage builds:** For production (advanced technique)
✅ **Security:** Don't hardcode secrets, use environment variables
✅ **Health checks:** Include health check commands for monitoring
✅ **Logging:** Ensure logs are visible outside container

---

## Next Steps (Chapter 9)

- Docker Compose: Run multiple containers together
- Container orchestration: Kubernetes basics
- Cloud deployment: AWS ECS, Google Cloud Run
- CI/CD integration: Automated builds and deployments

---

## Key Takeaways

🐳 **Docker:** Package → Distribute → Run anywhere identically
📦 **Image:** Blueprint containing code + dependencies
🏃 **Container:** Running instance of image
🔧 **Dockerfile:** Instructions to build image
📤 **Registry:** Storage for sharing images
🔌 **Port Mapping:** Connect container port to your machine's port
✅ **Consistency:** Same app, same behavior, any machine

---

**Ready to containerize your applications! 🚀**
