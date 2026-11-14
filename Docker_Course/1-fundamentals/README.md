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

## Interview Questions

**Q1: What's the main difference between Docker and Virtual Machines?**
A: VMs emulate entire OS; Docker shares host OS kernel, making containers lighter and faster.

**Q2: What's the difference between a Docker image and a container?**
A: Image is a blueprint (static file). Container is a running instance of that image.

**Q3: What is a Dockerfile?**
A: A text file with instructions to build a Docker image (FROM, RUN, COPY, CMD, etc.).

**Q4: What does `docker build` do?**
A: Reads Dockerfile and creates an image from it, following each instruction step-by-step.

**Q5: What does `docker run` do?**
A: Takes an image and creates/starts a new container from it.

**Q6: What's a Docker registry?**
A: A repository service that stores Docker images (Docker Hub, ECR, GCR, etc.).

**Q7: What's the difference between `ENTRYPOINT` and `CMD` in Dockerfile?**
A: ENTRYPOINT sets the main process; CMD provides default arguments (but can be overridden).

**Q8: What are Docker layers?**
A: Each Dockerfile instruction creates a layer. Layers stack to form the final image.

**Q9: How do you see a container's logs?**
A: Use `docker logs <container_id>` command.

**Q10: Can you have multiple containers running from the same image?**
A: YES! Each container is independent, even if from the same image.

---

## 🤔 Confusing Questions (Follow-Up Interview Questions)

### Q11: If you have 10 containers running from the same image, does each container have its own copy of files?

**Answer:**

NO! They share the image layers (read-only), but each has its own writable layer:

```
Image (shared, read-only):
├── Layer 1: Base OS files
├── Layer 2: Dependencies
└── Layer 3: App code

Container 1 (writable layer):
├── Changes made to files
└── New files created

Container 2 (writable layer):
├── Independent copy of changes
└── Independent files
```

**This saves disk space!** Multiple containers can run from one image efficiently.

---

### Q12: What happens if you `docker run` the same image twice without stopping the first container?

**Answer:**

Two separate containers run independently:

```bash
docker run my-app  # Container A starts
docker run my-app  # Container B starts (separate from A)

# Both running simultaneously, isolated from each other
docker ps
# CONTAINER ID | IMAGE   | STATUS
# abc123       | my-app  | Up 2 minutes
# def456       | my-app  | Up 1 minute
```

---

### Q13: Can you modify files inside a running container?

**Answer:**

YES! Changes go to the container's writable layer (not the image):

```bash
docker run -it ubuntu
# Inside container:
echo "Hello" > /data/file.txt  # ✅ Works

docker ps  # See the container
docker exec <container_id> cat /data/file.txt  # "Hello"

# But stop/remove the container, and changes are GONE
docker rm <container_id>  # Data lost!
```

**This is why you use volumes for persistent data.**

---

### Q14: If you change a Dockerfile and rebuild, do all images get updated?

**Answer:**

NO! Old images remain unchanged. Rebuild creates a NEW image:

```bash
# Build v1
docker build -t my-app:1.0 .
# Creates image: my-app:1.0

# Modify Dockerfile
# Build v2
docker build -t my-app:2.0 .
# Creates image: my-app:2.0

docker images
# REPOSITORY | TAG | IMAGE ID
# my-app     | 1.0 | abc123 (old, unchanged)
# my-app     | 2.0 | def456 (new)
```

---

### Q15: What does `FROM` in a Dockerfile mean?

**Answer:**

Base image that all layers build upon:

```dockerfile
FROM ubuntu:20.04  # Start with Ubuntu OS
FROM python:3.9    # Start with Python already installed
FROM alpine:latest # Start with lightweight Alpine

# Everything after FROM builds on this foundation
```

**If FROM is missing, Dockerfile is invalid!**

---

### Q16: Can you have a Dockerfile with no `RUN` commands?

**Answer:**

YES! But it would be useless:

```dockerfile
FROM ubuntu:20.04
COPY myfile.txt /app/

# No RUN, no CMD - what would container do?

# Usually you need:
FROM ubuntu:20.04
RUN apt-get install -y python3  # Install things
COPY myfile.txt /app/
CMD ["python3", "/app/script.py"]  # What to run
```

---

### Q17: If a `RUN` command in Dockerfile fails, does the build continue?

**Answer:**

NO! Build stops and fails:

```dockerfile
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3
RUN echo "Hello"  # ✅ Runs
RUN false  # ❌ FAILS - Build stops here!
RUN echo "This never runs"  # Not executed
```

---

### Q18: What's the difference between `docker stop` and `docker kill`?

**Answer:**

- **stop:** Graceful shutdown (SIGTERM signal)
- **kill:** Forceful termination (SIGKILL signal)

```bash
docker stop <container_id>   # ✅ Gives app time to cleanup
docker kill <container_id>   # ❌ Forces immediate termination

# Stop: App receives signal, saves state, exits
# Kill: Immediate termination, potential data loss
```

---

### Q19: Can you run a container and directly execute a different command?

**Answer:**

YES! Override the image's CMD:

```dockerfile
# In Dockerfile
CMD ["python", "app.py"]

# But you can override:
docker run my-app python debug.py  # ← Runs debug.py instead!
docker run my-app bash  # ← Opens bash instead of app.py!
```

---

### Q20: What happens if the `CMD` process in a container exits/crashes?

**Answer:**

Container stops automatically:

```bash
docker run my-app
# Container runs main process
# If process exits, container stops
# Container automatically removed if --rm flag used

# Container status:
docker ps  # Empty (not running)
docker ps -a  # Shows stopped container
```

**This is key:** Containers are tied to their main process. No process = no container.

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
