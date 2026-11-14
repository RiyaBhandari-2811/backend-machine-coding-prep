# Chapter 8: Dockerizing the FastAPI Insurance API

**Quick Start:** Build and run your FastAPI application as a Docker container

## 🎯 What You'll Learn

- Create a Dockerfile for Python FastAPI applications
- Build Docker images from your code
- Push images to Docker Hub for sharing
- Pull and run images locally
- Test Dockerized applications

## 📋 Prerequisites

- ✅ Completed Chapter 7 (Improved API)
- ✅ Docker Desktop installed ([download here](https://www.docker.com/products/docker-desktop/))
- ✅ Docker Hub account ([sign up here](https://hub.docker.com))
- ✅ Basic Docker knowledge (see Docker_Course if needed)

## ⏱️ Time Required

- **Learning:** 20-30 minutes
- **Hands-on:** 30-40 minutes
- **Total:** 60 minutes

## 📁 Required Files

Your chapter7 folder should already have:
```
chapter7/
├── main.py                          ✓ From Chapter 7
├── requirements.txt                 ✓ From Chapter 7
├── schemas/
│   ├── user_input.py               ✓
│   └── prediction_response.py       ✓
├── config/
│   └── city_tier.py                ✓
├── models/
│   ├── predict.py                  ✓
│   └── model.pkl                   ✓
├── Dockerfile                       ← CREATE THIS
├── .dockerignore                    ← CREATE THIS
└── chapter8.md                      ← REFERENCE GUIDE
```

## 🚀 Quick Steps

### 1. Create Dockerfile

In `FastAPI_Course/chapter7/` create a file named `Dockerfile` (no extension):

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create .dockerignore

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
.venv/
.env
.git
.gitignore
.dockerignore
*.md
.pytest_cache
.coverage
```

### 3. Build the Image

```bash
cd FastAPI_Course/chapter7/

docker build -t YOUR_USERNAME/insurance-api:1.0 .
```

Replace `YOUR_USERNAME` with your Docker Hub username.

### 4. Test Locally

```bash
# Run the container
docker run -d -p 8000:8000 --name insurance-api YOUR_USERNAME/insurance-api:1.0

# Visit http://localhost:8000
# Visit http://localhost:8000/docs for Swagger UI
```

### 5. Push to Docker Hub

```bash
# Login
docker login

# Push
docker push YOUR_USERNAME/insurance-api:1.0
```

### 6. Pull and Run (Simulate Tester)

```bash
# Clean local image
docker rmi YOUR_USERNAME/insurance-api:1.0

# Pull from Docker Hub
docker pull YOUR_USERNAME/insurance-api:1.0

# Run
docker run -d -p 8000:8000 YOUR_USERNAME/insurance-api:1.0
```

## 🧪 Testing Endpoints

### Health Check
```
GET http://localhost:8000/health
```

### Predict Insurance Premium
```
POST http://localhost:8000/predict
Content-Type: application/json

{
  "age": 31,
  "weight": 91,
  "height": 1.72,
  "income_lpa": 10,
  "smoker": true,
  "city": "gurgaon",
  "occupation": "retired"
}
```

### Interactive Documentation
```
http://localhost:8000/docs
```

## 🔑 Key Concepts

| Term | Meaning |
|------|---------|
| **Dockerfile** | Instructions for building a Docker image |
| **Image** | Packaged application with all dependencies (blueprint) |
| **Container** | Running instance of an image (executable) |
| **Docker Hub** | Registry for sharing Docker images |
| **Layer** | Individual step in image building (cached for speed) |

## 🛠️ Common Commands

```bash
# Build image
docker build -t name:tag .

# Run container
docker run -d -p host_port:container_port name:tag

# View running containers
docker ps

# View all containers
docker ps -a

# View images
docker images

# Stop container
docker stop container_id

# Remove container
docker rm container_id

# View logs
docker logs container_id

# Login to Docker Hub
docker login

# Push to Docker Hub
docker push username/image:tag

# Pull from Docker Hub
docker pull username/image:tag
```

## 📊 Before vs After

### Before Docker
```
Developer's Machine:     ✅ Works
Colleague's Machine:     ❌ Dependencies missing
Tester's Machine:        ❌ Wrong Python version
Production Server:       ❌ Deployment fails
```

### After Docker
```
Developer's Machine:     ✅ Works identically
Colleague's Machine:     ✅ Works identically
Tester's Machine:        ✅ Works identically
Production Server:       ✅ Works identically
```

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| Docker daemon not running | Start Docker Desktop |
| Port 8000 already in use | Use `docker run -p 8001:8000 ...` |
| Can't login to Docker Hub | Run `docker logout` then `docker login` |
| Image build fails | Verify all files are in chapter7 directory |
| Container exits immediately | Run `docker logs container_id` |

## 📚 Related Topics

### Docker Fundamentals
See **Docker_Course/1-fundamentals/** for:
- Docker concepts and architecture
- How images and containers work
- Comparison with alternatives (VMs, Kubernetes, etc.)

### Advanced Docker Topics
See **Docker_Course/2-practical/** for:
- Multi-container applications
- docker-compose orchestration
- Best practices

### Production Deployment
See **Docker_Course/4-deployment/** for:
- AWS ECS deployment
- Kubernetes basics
- CI/CD integration

## ✅ Checklist

- [ ] Docker Desktop installed and running
- [ ] Docker Hub account created
- [ ] Dockerfile created in chapter7/
- [ ] .dockerignore created in chapter7/
- [ ] Image built successfully
- [ ] Local container running and tested
- [ ] Logged in to Docker Hub
- [ ] Image pushed to Docker Hub
- [ ] Can pull and run from Docker Hub
- [ ] All endpoints working

## 🎓 Exercises

### Exercise 1: Build Your Image (10 min)
1. Navigate to chapter7 directory
2. Create Dockerfile and .dockerignore
3. Build the image with your username
4. View in Docker Desktop

### Exercise 2: Local Testing (15 min)
1. Run the container locally
2. Test all endpoints with curl or browser
3. Check logs
4. Stop and remove container

### Exercise 3: Publish to Docker Hub (15 min)
1. Login to Docker Hub
2. Push your image
3. Verify on hub.docker.com
4. Share link with a friend

### Exercise 4: Pull and Run (10 min)
1. Delete local image
2. Pull from Docker Hub
3. Run the pulled image
4. Verify everything works

## 🌟 Next Chapter Preview

**Chapter 9: AWS Deployment**
- Deploy your Docker image to AWS ECS
- Make it accessible on the internet
- Public URL: `https://your-api.example.com/predict`
- Auto-scaling and load balancing

## 📖 Full Guide

See **[chapter8.md](./chapter8.md)** for complete detailed guide with:
- Step-by-step instructions
- Deep explanations
- Interview questions
- Troubleshooting guide
- Best practices

## 🎯 Learning Path

```
Chapter 1-6: API Fundamentals
         ↓
Chapter 7: Production-Grade API ← You are here
         ↓
Chapter 8: Dockerization ← Hands-on task
         ↓
Chapter 9: Cloud Deployment (Coming next)
         ↓
Complete FastAPI Mastery! 🚀
```

## 💡 Key Takeaway

Docker solves the "it works on my machine" problem by packaging your entire application with all its dependencies into a container that works identically anywhere.

**Your Docker image = Ship it anywhere = Works everywhere** ✅

---

**Time to Complete:** 60 minutes  
**Difficulty:** Intermediate  
**Hands-on Requirement:** Yes (Build, Test, Push)  
**Next:** Chapter 9 - AWS ECS Deployment
