# Module 1: Docker Fundamentals (45 minutes)

## Overview
This module covers the core concepts and architecture of Docker, essential for understanding containerization.

**Time allocation:** 45 minutes  
**Topics:** 8  
**Files:** 3 markdown guides

---

## Topics Covered

### 1. What is Docker? (5 min)
- Definition and purpose
- Why containerization matters
- Real-world analogies
- Comparison with traditional deployment

**Key concept:** Docker packages application + dependencies into isolated containers

**File:** `docker-concepts.md` - Section 1

---

### 2. Docker Architecture (8 min)
- Docker Engine components
- Client-Server model
- Docker daemon
- REST API

**Key concept:** Docker works as daemon + CLI client architecture

**File:** `docker-architecture.md` - Complete

---

### 3. Core Concepts (10 min)
- **Image:** Blueprint/template (like a class)
- **Container:** Running instance (like an object)
- **Registry:** Image storage (like GitHub)
- **Dockerfile:** Instructions to build image
- **Layers:** Incremental building blocks

**Key concept:** Image is static, container is dynamic

**File:** `docker-concepts.md` - Section 2

---

### 4. Dockerfile Basics (8 min)
- Essential instructions: FROM, WORKDIR, COPY, RUN, EXPOSE, CMD
- Build process explained
- Layer caching
- Best practices

**Key concept:** Dockerfile = Recipe for creating Docker image

**File:** `docker-concepts.md` - Section 3

---

### 5. Docker Workflow (5 min)
- Write Dockerfile
- Build image
- Create container
- Run container

**Key concept:** Dockerfile → Image → Container

**File:** `docker-concepts.md` - Section 4

---

### 6. Comparison: Docker vs Alternatives (5 min)
- Docker vs Virtual Machines
- Docker vs Kubernetes
- When to use Docker
- When to use alternatives

**Key concept:** Docker is lightweight, fast, easy to use

**File:** `docker-vs-alternatives.md` - Complete

---

### 7. Installation Verification (3 min)
- Verify Docker installation
- Hello-world container
- Check version and info
- Common issues

**Key concept:** Ensure Docker is ready before practical work

**File:** See SETUP.md in parent directory

---

### 8. Quick Start (1 min)
- First container in 30 seconds
- Accessing application

**Key concept:** Get hands-on immediately

**File:** `docker-concepts.md` - Quick Start section

---

## Learning Path

```
1. Read: docker-concepts.md (What is Docker + Core Concepts)
         ↓
2. Understand: Docker Architecture (docker-architecture.md)
         ↓
3. Learn: Dockerfile and build process (docker-concepts.md)
         ↓
4. Compare: Docker vs Alternatives (docker-vs-alternatives.md)
         ↓
5. Practice: Run your first container
         ↓
6. Move to: Module 2 (Practical Implementation)
```

---

## Key Takeaways

✅ Docker is a containerization platform  
✅ Image = Template, Container = Running instance  
✅ Dockerfile contains instructions to build images  
✅ Docker is lightweight and faster than VMs  
✅ Docker enables consistent development/production environments  
✅ Registry (Docker Hub) stores and shares images  

---

## Terminology Quick Reference

| Term | Meaning |
|------|---------|
| Image | Blueprint for containers |
| Container | Running instance of image |
| Dockerfile | Recipe to create image |
| Registry | Storage for images (Docker Hub) |
| Layer | Step in image build process |
| Daemon | Background service managing containers |
| Client | Docker CLI used to issue commands |

---

## Quick Commands (Fundamentals)

```bash
# Build image
docker build -t myapp:1.0 .

# Run container
docker run -d -p 8000:5000 myapp:1.0

# List containers
docker ps -a

# View logs
docker logs container_id

# Stop container
docker stop container_id

# Remove container
docker rm container_id
```

See CHEATSHEET.md for complete command reference.

---

## Practice Exercise

**After completing this module, you should be able to:**

1. ✅ Explain what Docker is in 30 seconds
2. ✅ Describe the difference between image and container
3. ✅ Write a basic Dockerfile
4. ✅ Build a Docker image
5. ✅ Run a container from your image
6. ✅ View container logs
7. ✅ Stop and remove containers

**Exercise:** 
- Create a simple Python app
- Write Dockerfile for it
- Build image
- Run container
- Access application

---

## Next Steps

→ Continue to **Module 2: Practical Implementation**

Where you'll learn:
- Real-world applications
- Multiple examples
- Docker Compose basics
- Best practices in action

---

## Resources

- Full setup guide: See [SETUP.md](../SETUP.md)
- Command reference: See [CHEATSHEET.md](../CHEATSHEET.md)
- Interview Q&A: See [interview-questions.md](../interview-questions.md)
- Course index: Back to [README.md](../README.md)

---

**Estimated time to complete:** 45 minutes  
**Recommended approach:** Read files in order, practice commands as you go
