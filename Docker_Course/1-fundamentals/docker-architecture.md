# Docker Architecture & How It Works

## Table of Contents
1. [Docker Architecture Overview](#docker-architecture-overview)
2. [Docker Daemon](#docker-daemon)
3. [Docker Client](#docker-client)
4. [Docker Objects](#docker-objects)
5. [How Docker Works](#how-docker-works)
6. [Containerization Technology](#containerization-technology)

---

## Docker Architecture Overview

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     YOUR MACHINE (HOST)                      │
├──────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Docker CLI │  │  Docker GUI  │  │ Docker API   │       │
│  │  (Command    │  │  (Desktop    │  │ (REST API)   │       │
│  │   line)      │  │   app)       │  │              │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                  │               │
│         └─────────────────┼──────────────────┘               │
│                           │ (requests)                        │
│         ┌─────────────────↓──────────────────┐               │
│         │    DOCKER DAEMON (dockerd)         │               │
│         │  - Manages containers              │               │
│         │  - Manages images                  │               │
│         │  - Manages networks                │               │
│         │  - Manages volumes                 │               │
│         └──────────┬─────────┬───────────────┘               │
│         ┌──────────↓────────┐│                               │
│         │   Container 1     │└──────────────────┐            │
│         │ (Python + Flask)  │  Container 2     │            │
│         │  Process 1        │  (Node.js)       │            │
│         │  Process 2        │  Process 1       │            │
│         │  Isolated FS      │  Process 2       │            │
│         │  Network          │  Isolated FS     │            │
│         └───────────────────┤  Network         │            │
│                             └──────────────────┘            │
│  ┌───────────────────────────────────────────────┐           │
│  │         HOST KERNEL (Linux, Windows, macOS)    │           │
│  │  - Manages processes                           │           │
│  │  - Manages memory                              │           │
│  │  - Manages networking                          │           │
│  └───────────────────────────────────────────────┘           │
└──────────────────────────────────────────────────────────────┘
```

### Client-Server Model

Docker uses **Client-Server architecture**:

```
CLIENT SIDE                       SERVER SIDE
─────────────                     ───────────

Docker CLI                         Docker Daemon
   ↓                                   ↑
docker build                        Builds image
docker run                          Runs container
docker pull                         Pulls from registry
docker exec                         Executes command
docker logs                         Returns logs
   ↓                                   ↑
  HTTP REST API                    Listens on port
                                   (Unix socket or TCP)
```

**How it works:**
1. You run: `docker run myapp:1.0`
2. Docker CLI sends request to Docker daemon
3. Daemon processes request
4. Daemon returns response to CLI
5. CLI displays output to you

---

## Docker Daemon

### What is the Docker Daemon?

The **Docker daemon** (dockerd) is a background service that:
- Listens for Docker API requests
- Manages Docker objects (images, containers, networks, volumes)
- Communicates with other daemons to manage Docker services
- Handles all the heavy lifting

### Where Does It Run?

**Linux:** Runs as system service
```bash
# Check daemon status
systemctl status docker

# Start daemon
sudo systemctl start docker

# Daemon runs in background
sudo systemctl enable docker  # Auto-start on boot
```

**macOS/Windows:** Runs inside virtual machine (via Docker Desktop)
```
Your machine → Docker Desktop → VM → Docker daemon
                 (GUI)         (Linux)
```

### Docker Daemon Responsibilities

1. **Image Management**
   - Building images from Dockerfile
   - Storing images locally
   - Pulling/pushing from registries

2. **Container Lifecycle**
   - Creating containers
   - Starting/stopping containers
   - Removing containers
   - Managing container resources

3. **Networking**
   - Creating networks
   - Connecting containers
   - Port mapping
   - DNS resolution

4. **Storage**
   - Managing volumes
   - Managing bind mounts
   - Handling filesystem isolation

5. **Logging**
   - Collecting container logs
   - Storing log data
   - Providing log access

---

## Docker Client

### What is Docker Client?

The **Docker client** is your interface to Docker daemon. It's what you interact with.

### Access Methods

**1. Docker CLI (Command Line)**
```bash
docker --version
docker run myapp:1.0
docker logs container_id
docker ps
```

**2. Docker Desktop GUI**
- Visual interface for Docker
- View containers, images, volumes
- Manage resources
- View logs
- Access settings

**3. Docker API (Programmatic)**
```bash
# Using curl (HTTP REST API)
curl http://localhost:2375/containers/json

# Using Python
import docker
client = docker.from_env()
containers = client.containers.list()
```

**4. IDE Plugins**
- VS Code extension
- IntelliJ Docker plugin
- Others

### Docker CLI Examples

```bash
# Version info
docker --version
docker info

# Image commands
docker pull python:3.9
docker build -t myapp:1.0 .
docker images

# Container commands
docker run myapp:1.0
docker ps
docker logs container_id
docker exec -it container_id bash

# Network commands
docker network ls
docker network inspect mynetwork

# Volume commands
docker volume ls
docker volume inspect myvolume
```

---

## Docker Objects

### 1. Images

**What:** Lightweight, standalone executable package containing everything needed to run code.

**Properties:**
- Read-only (immutable)
- Built from layers
- Stored locally or in registry
- Can be tagged with versions

**Lifecycle:**
```
Build → Store Locally → Push to Registry → Others pull → Run
```

**Image locations:**
```
/var/lib/docker/image/overlay2/  (Linux)
~/Library/Containers/com.docker.docker/Data/  (macOS)
C:\Users\YourName\AppData\Local\Docker\  (Windows)
```

---

### 2. Containers

**What:** Runtime instance of an image. It's like a process.

**Properties:**
- Running instance of image
- Has state (running, stopped, etc.)
- Isolated environment
- Temporary by default (deleted when stopped)

**Lifecycle:**
```
Created → Running → Paused → Stopped → Removed

docker run ──→ Container running
docker stop ──→ Container stopped (can restart)
docker rm ──→ Container removed (gone forever)
```

**Container storage:**
```
/var/lib/docker/containers/  (Linux)
~/Library/Containers/com.docker.docker/Data/containers/  (macOS)
```

---

### 3. Networks

**What:** Enable communication between containers and with the host.

**Network types:**
1. **Bridge:** Default, isolated network
2. **Host:** Uses host's network (Linux only)
3. **None:** No network connectivity
4. **Overlay:** For Docker Swarm
5. **Macvlan:** Advanced networking

**Example:**
```bash
# Create network
docker network create mynet

# Connect containers to network
docker run --network mynet --name web myapp:1.0
docker run --network mynet --name db postgres:13

# Containers can communicate: web → db:5432
```

---

### 4. Volumes

**What:** Persist data outside containers.

**Three types:**
1. **Named volumes:** Managed by Docker
2. **Bind mounts:** Direct path mapping
3. **tmpfs:** In-memory storage

**Example:**
```bash
# Named volume
docker volume create mydata
docker run -v mydata:/app/data myapp:1.0

# Bind mount
docker run -v /host/path:/app/data myapp:1.0
```

**Volume storage:**
```
/var/lib/docker/volumes/  (Linux)
~/Library/Containers/.../volumes/  (macOS)
```

---

## How Docker Works

### Step-by-Step: Running a Container

**Command:**
```bash
docker run -p 8000:5000 -e DEBUG=True python:3.9 python app.py
```

**Behind the scenes:**

```
Step 1: Check if image exists locally
        ├─ Found? → Continue to Step 2
        └─ Not found? → Pull from Docker Hub → Step 2

Step 2: Create container from image
        ├─ Allocate filesystem
        ├─ Set up networking
        ├─ Configure environment variables
        ├─ Set up volumes
        └─ Continue to Step 3

Step 3: Configure port mapping
        ├─ Map host port 8000 → container port 5000
        └─ Continue to Step 4

Step 4: Create namespaces and cgroups
        ├─ Process namespace (isolated PIDs)
        ├─ Network namespace (isolated network stack)
        ├─ Filesystem namespace (isolated filesystem)
        ├─ IPC namespace (isolated communication)
        ├─ Mount namespace (isolated mounts)
        ├─ User namespace (isolated user IDs)
        └─ Continue to Step 5

Step 5: Start container process
        ├─ Execute: python app.py
        ├─ Process runs in container
        └─ Container is now RUNNING

Step 6: Attach to container (if interactive)
        └─ Display output, accept input

Container stops when main process (python app.py) exits
```

---

### Image Layers in Detail

**Building an image:**
```dockerfile
FROM python:3.9
RUN pip install flask
COPY app.py /app/
CMD ["python", "app.py"]
```

**Layer creation:**
```
Layer 1: FROM python:3.9
         ├─ Pulls base image from registry
         └─ Size: ~900MB (Python runtime)

Layer 2: RUN pip install flask
         ├─ Runs command in Layer 1
         ├─ Installs Flask
         └─ Size: +50MB

Layer 3: COPY app.py /app/
         ├─ Copies file from host
         └─ Size: +5KB

Layer 4: CMD ["python", "app.py"]
         ├─ Sets default command
         └─ Size: 0 (metadata only)

Final image: ~950MB (all layers stacked)
```

**Caching example:**
```
Build 1: All layers built (no cache)
         Time: 60 seconds
         
Build 2 (no changes): All cached
         Time: 1 second
         
Build 3 (code changed - app.py): 
         Layer 1-2: Cached
         Layer 3: Fresh build (code changed)
         Layer 4: Rebuilds (depends on changed layer)
         Time: 5 seconds
```

---

## Containerization Technology

### Linux Kernel Features

Docker uses Linux kernel features for isolation:

**1. Namespaces**
Isolate system resources for each container.

```
PID Namespace:      Container A sees PIDs 1-100
                    Container B sees PIDs 1-50
                    Same PIDs on host: 500-599

Network Namespace:  Container A: eth0 with IP 172.17.0.2
                    Container B: eth0 with IP 172.17.0.3
                    Isolated network stacks

Filesystem:         Container A: /app (its own root)
                    Container B: /app (different root)

IPC Namespace:      Container A: Isolated message queues
                    Container B: Isolated message queues
```

**2. Control Groups (cgroups)**
Limit and monitor resources.

```
Container A:
├─ CPU: Max 0.5 cores
├─ Memory: Max 512MB
└─ I/O: Limit disk usage

Container B:
├─ CPU: Max 1 core
├─ Memory: Max 1GB
└─ I/O: Limit disk usage

Result: Fair resource allocation
```

**3. Union File Systems**
Stack multiple filesystems efficiently.

```
Layer 3 (read-write): Your changes
      ↓
Layer 2 (read-only): Application code
      ↓
Layer 1 (read-only): Python runtime
      ↓
Kernel (read-only): Linux kernel
```

---

### Isolation Visualization

```
Virtual Machine:
┌─────────────────┐
│ Full OS (5GB)   │
│ App Runtime     │
│ Application     │
│ Libraries       │
└─────────────────┘
   ← Runs separately

Docker Container:
┌─────────────────┐
│ Application     │
│ Libraries       │
└─────────────────┘ ← Shares kernel
   ↓ ↓ ↓ ↓
Shared Linux Kernel (lightweight)

Result:
VM: 5GB, boots in minutes
Container: 50MB, starts in seconds
```

---

### How Port Mapping Works

**Without port mapping:**
```
Your machine (host)
Port 5000 → ❌ Nothing

Container
Port 5000 → Flask app listening
```

**With port mapping (-p 8000:5000):**
```
Your machine (host)
Port 8000 → ✅ Redirected to container port 5000

Docker Daemon (port mapping logic)
Host port 8000 ← → Container port 5000
                  (iptables rules)

Container
Port 5000 → ✅ Flask app listening

Result:
curl http://localhost:8000 → Works! (redirected to container:5000)
```

---

### How Volume Mounting Works

**Without volume:**
```
Container filesystem: /app/data/file.txt
Container stops → /app/data/file.txt deleted ❌
```

**With named volume (-v myvolume:/app/data):**
```
Host storage: /var/lib/docker/volumes/myvolume/_data/file.txt

Container sees: /app/data/file.txt (mounted)

Container stops → File still exists in host storage ✅
New container: -v myvolume:/app/data → Can access same file ✅
```

**With bind mount (-v /host/path:/app/data):**
```
Host path: /Users/me/data/file.txt

Container sees: /app/data/file.txt (mounted)

Container stops → File still in host path ✅
Direct access from host → Can edit file ✅
```

---

## Docker Daemon Communication

### Unix Socket (Default on Linux/macOS)

```bash
# Docker CLI connects via Unix socket
/var/run/docker.sock

# You can interact with daemon:
curl --unix-socket /var/run/docker.sock http://localhost/containers/json
```

### TCP Socket (Docker Desktop, Remote)

```bash
# Docker daemon listens on TCP port
DOCKER_HOST=tcp://localhost:2375

# Remote machine:
export DOCKER_HOST=tcp://192.168.1.100:2375
docker ps  # Controls remote daemon
```

---

## Architecture Summary

**Key Components:**

| Component | Role |
|-----------|------|
| Docker Daemon | Background service managing everything |
| Docker Client | Your interface (CLI, GUI, API) |
| Images | Blueprints (read-only) |
| Containers | Running instances |
| Registries | Image storage |
| Networks | Container communication |
| Volumes | Data persistence |

**Technology Stack:**
- Namespaces: Process isolation
- Cgroups: Resource limits
- Union FS: Layered filesystem
- iptables: Port mapping
- Overlay networks: Container networking

**Communication:**
```
You → Docker CLI → Unix/TCP Socket → Docker Daemon → OS kernel
```

---

## Next Steps

- Understand fundamental concepts ✅
- Understand architecture ✅
- Compare with alternatives → `docker-vs-alternatives.md`
- Practice with real examples → Module 2

---

**Ready to compare with alternatives?** → `docker-vs-alternatives.md`
