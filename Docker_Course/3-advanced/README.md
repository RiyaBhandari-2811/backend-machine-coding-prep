# Module 3: Advanced Docker Topics (40+ minutes)

## Overview
This module covers advanced Docker features, best practices, and production-grade concepts.

**Time allocation:** 40+ minutes  
**Topics:** 10  
**Files:** 5 comprehensive guides

---

## Topics Covered

### 1. Docker Compose Advanced Features (8 min)
- Override files
- Profiles (dev/prod/test)
- Health checks in compose
- Restart policies
- Resource limits
- Advanced networking

**File:** `docker-compose-guide.md`

---

### 2. Docker Networking (8 min)
- Network drivers (bridge, host, overlay, macvlan)
- Custom networks
- Container communication
- Port publishing
- DNS resolution
- Network troubleshooting

**File:** `networking.md`

---

### 3. Volumes & Storage (8 min)
- Named volumes vs bind mounts
- Volume drivers
- Data persistence strategies
- Backup and restore
- Volume cleanup
- Storage optimization

**File:** `volumes-storage.md`

---

### 4. Docker Security (8 min)
- Running as non-root user
- Secret management
- Image scanning
- Network isolation
- Resource limits
- Compliance and best practices

**File:** `security.md`

---

### 5. Performance Optimization (8 min)
- Image size reduction
- Layer caching strategy
- Build optimization
- Runtime performance
- Resource allocation
- Monitoring metrics

**File:** `optimization.md`

---

### 6. Docker Compose in Production (5 min)
- Stack deployment
- High availability
- Load balancing
- Backup strategies
- Monitoring and logging
- Disaster recovery

**Covered in:** `docker-compose-guide.md` (Advanced section)

---

### 7. Multi-Container Orchestration (5 min)
- Complex relationships
- Service dependencies
- Init containers
- Sidecar patterns
- Job scheduling

**Covered in:** `docker-compose-guide.md` (Patterns section)

---

### 8. Logging & Monitoring (5 min)
- Log drivers (json-file, syslog, awslogs, etc.)
- Log aggregation
- Metrics collection
- Health monitoring
- Alerting strategies

**Covered in:** Advanced sections

---

### 9. CI/CD Integration (5 min)
- Automated image building
- Push to registry
- Pull in production
- Deployment automation
- Rollback strategies

**Covered in:** Reference

---

### 10. Container Registry Management (2 min)
- Docker Hub organization
- Private registries
- Image versioning
- Cleanup strategies
- Access control

**Covered in:** Reference

---

## File Structure

```
3-advanced/
├── README.md (this file)
├── docker-compose-guide.md (comprehensive)
├── networking.md (network drivers, DNS, troubleshooting)
├── volumes-storage.md (volume types, strategies)
├── security.md (hardening, secrets, scanning)
└── optimization.md (performance, tuning)
```

---

## Learning Path

```
1. Docker Compose Advanced
   Read: docker-compose-guide.md
   Understand: Profiles, overrides, health checks
   Practice: Create compose file with prod config
         ↓

2. Networking
   Read: networking.md
   Understand: Network drivers, DNS, communication
   Practice: Custom network, service discovery
         ↓

3. Volumes & Storage
   Read: volumes-storage.md
   Understand: Volume types, persistence strategies
   Practice: Named volume, bind mount, backup/restore
         ↓

4. Security
   Read: security.md
   Understand: User permissions, secrets, scanning
   Practice: Run container as non-root, scan images
         ↓

5. Optimization
   Read: optimization.md
   Understand: Image size, caching, performance
   Practice: Multi-stage build, measure impact
         ↓

6. Next: Module 4 (Deployment & Production)
```

---

## Key Advanced Concepts

### 1. Override Compose Files

```bash
# Base configuration
docker-compose -f docker-compose.yml up

# Override for production
docker-compose -f docker-compose.yml \
               -f docker-compose.prod.yml up

# Override for development
docker-compose -f docker-compose.yml \
               -f docker-compose.dev.yml up
```

### 2. Docker Compose Profiles

```yaml
version: '3.8'
services:
  web:
    image: web:1.0
    profiles:
      - prod
      - dev
  
  db:
    image: postgres:13
    profiles:
      - prod
  
  debug-tools:
    image: debug:1.0
    profiles:
      - dev
```

```bash
# Start only prod services
docker-compose --profile prod up

# Start only dev services
docker-compose --profile dev up
```

### 3. Network Drivers

```
Bridge (default):
Container A ←→ Container B (isolated network)

Host:
Container processes appear as host processes

Overlay:
Container A (Host 1) ←→ Container B (Host 2) (Swarm/K8s)

Macvlan:
Container gets MAC address (advanced)
```

### 4. Volume Strategies

```
Development:
docker run -v $(pwd):/app  # Bind mount (hot reload)

Production:
docker run -v named_vol:/data  # Named volume (persistence)

Temporary:
docker run --tmpfs /tmp  # In-memory (ephemeral)
```

### 5. Security Layers

```
1. Run as non-root user
2. Use read-only filesystem
3. Limit capabilities
4. Resource limits (memory, CPU)
5. Network isolation
6. Secret management (not env vars)
7. Regular scanning for vulnerabilities
8. Keep base images updated
```

---

## Advanced Exercises

### Exercise 1: Compose Profiles
**Time:** 10 minutes
1. Create docker-compose.yml with multiple services
2. Add profiles: prod, dev, testing
3. Run with different profiles
4. Observe which services start
5. Override specific services per profile

**Learning:** Production-like configuration management

### Exercise 2: Custom Network
**Time:** 8 minutes
1. Create custom bridge network
2. Run multiple containers on network
3. Verify communication by name (DNS)
4. Inspect network
5. Disconnect container

**Learning:** Container networking, service discovery

### Exercise 3: Volume Management
**Time:** 8 minutes
1. Create named volume
2. Run container with volume
3. Write data inside
4. Stop container
5. Create new container with same volume
6. Verify data persists
7. Backup volume
8. Restore to new volume

**Learning:** Data persistence, backup/restore

### Exercise 4: Security Hardening
**Time:** 8 minutes
1. Create Dockerfile with non-root user
2. Add resource limits in compose
3. Use read-only root filesystem
4. Scan image for vulnerabilities
5. Compare before/after

**Learning:** Production security practices

### Exercise 5: Performance Optimization
**Time:** 8 minutes
1. Create Dockerfile with poor practices
2. Measure image size
3. Apply optimization techniques
4. Measure new size
5. Compare layer count
6. Benchmark build time

**Learning:** Performance tuning

---

## Common Advanced Patterns

### Pattern 1: Development vs Production

**docker-compose.yml (shared):**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./app:/app
```

**docker-compose.prod.yml (production overrides):**
```yaml
version: '3.8'
services:
  web:
    image: myregistry.azurecr.io/web:1.0
    ports:
      - "80:5000"
    volumes: []  # No mount in prod
    restart_policy:
      condition: on-failure
      max_attempts: 3
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

### Pattern 2: Sidecar Container

```yaml
services:
  app:
    image: app:1.0
    volumes:
      - logs:/var/log/app
  
  log-aggregator:
    image: filebeat:1.0
    volumes:
      - logs:/var/log/app:ro
    depends_on:
      - app
```

### Pattern 3: Init Container Pattern

```yaml
services:
  database:
    image: postgres:13
    
  migrations:
    image: app:1.0
    command: python migrate.py
    depends_on:
      - database
  
  web:
    image: app:1.0
    depends_on:
      - migrations
```

### Pattern 4: Rolling Update

```bash
# Old approach (downtime)
docker-compose down
docker-compose up

# Better approach (rolling)
docker-compose up -d web=5  # 5 instances
docker tag newapp:2.0 registry/app:2.0
docker-compose up -d  # Gradually updates
```

---

## Troubleshooting Advanced Issues

### Issue 1: Containers Can't Communicate

**Symptoms:** Connection refused between containers

**Solution:**
```bash
# Check network
docker network ls

# Create network
docker network create mynet

# Connect containers
docker run --network mynet app:1.0

# Verify DNS
docker exec container_id nslookup other_container
```

### Issue 2: Volume Permission Issues

**Symptoms:** Permission denied accessing mounted volume

**Solution:**
```dockerfile
# Dockerfile
RUN chown -R appuser:appuser /app
USER appuser
```

### Issue 3: Out of Disk Space

**Symptoms:** Disk full error

**Solution:**
```bash
# Clean up
docker system prune -a
docker volume prune

# Check disk usage
docker system df

# Remove specific items
docker rmi image_id
docker volume rm volume_id
```

### Issue 4: Performance Degradation

**Symptoms:** Containers running slow

**Solution:**
```bash
# Check resource usage
docker stats

# Check logs
docker logs -f container_id

# Profile application
docker run --cap-add SYS_ADMIN app:debug

# Measure disk I/O
docker run --device /dev/sda app:benchmark
```

---

## Performance Benchmarking

### Measure Image Size
```bash
docker images | grep myapp

# Example output:
# REPOSITORY   TAG   SIZE
# myapp        1.0   250MB

# After optimization:
# REPOSITORY   TAG   SIZE
# myapp        2.0   80MB  (68% reduction)
```

### Measure Build Time
```bash
time docker build -t myapp:1.0 .

# Before: ~45 seconds
# After optimization: ~12 seconds
```

### Measure Runtime Performance
```bash
docker run --cpus 1 --memory 512m myapp:1.0

# Monitor during run
docker stats container_id
```

---

## Next Steps

→ Continue to **Module 4: Deployment & Production**

Where you'll learn:
- AWS ECS deployment
- Google Cloud deployment
- Kubernetes basics
- CI/CD integration
- Interview preparation

---

## Deep Dive Resources

- Docker Compose advanced: `docker-compose-guide.md`
- Networking deep dive: `networking.md`
- Volume strategies: `volumes-storage.md`
- Security hardening: `security.md`
- Performance tuning: `optimization.md`

---

**Estimated time to complete:** 40-60 minutes  
**Recommended approach:** Read all guides + do all 5 exercises
