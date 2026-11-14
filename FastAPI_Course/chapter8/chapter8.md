# Chapter 8: Dockerizing the Insurance Premium Prediction API

## Overview
In this chapter, we'll take the improved FastAPI application from Chapter 7 and containerize it using Docker. We'll build a Docker image, push it to Docker Hub, and demonstrate how it can be run on any machine without any setup hassles.

**Prerequisites:** 
- Completed Chapter 7 (Improved API)
- Docker basics knowledge (refer Docker_Course Module 1 if needed)
- Docker Desktop installed
- Docker Hub account

**Time to complete:** 30-40 minutes

---

## Learning Objectives

By the end of this chapter, you'll be able to:

✅ Create a Dockerfile for FastAPI application  
✅ Build a Docker image from the application  
✅ Push the image to Docker Hub  
✅ Pull and run the image from Docker Hub  
✅ Test the Dockerized API  
✅ Understand the benefits of containerization  

---

## Why Docker?

### The Problem Without Docker

```
Developer's Machine: ✅ Works perfectly
Colleague's Machine: 😅 "It works on my machine"
Tester's Machine: 💥 Broken - missing dependencies
Production Server: 🔥 Complete failure - different Python version
```

### The Solution With Docker

```
Developer builds image → Colleague runs same image → Tester uses same image → Production deploys same image
Result: Works identically everywhere! ✅
```

---

## Step 1: Setup Required

### Prerequisites Check

**1. Docker Desktop Installation**

Visit https://www.docker.com/products/docker-desktop/ and install for your OS:
- Windows
- macOS
- Linux

**2. Docker Hub Account**

Create account at https://hub.docker.com if you don't have one.

**3. Verify Installation**

```bash
docker --version
docker run hello-world
```

---

## Step 2: Create Dockerfile

### What is Dockerfile?

A Dockerfile is an instruction manual that tells Docker how to build your image step-by-step, layer by layer.

### Dockerfile for Our API

Create a file named `Dockerfile` (capital D, no extension) in your FastAPI_Course/chapter7/ directory:

```dockerfile
# Step 1: Start with Python base image
FROM python:3.9-slim

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Copy requirements file
COPY requirements.txt .

# Step 4: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy application code
COPY . .

# Step 6: Set environment variable to avoid buffering
ENV PYTHONUNBUFFERED=1

# Step 7: Expose port 8000
EXPOSE 8000

# Step 8: Run the API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile Explanation

| Instruction | Purpose |
|-------------|---------|
| `FROM python:3.9-slim` | Start with lightweight Python 3.9 base image |
| `WORKDIR /app` | Set working directory inside container |
| `COPY requirements.txt .` | Copy dependencies list |
| `RUN pip install...` | Install all Python packages |
| `COPY . .` | Copy all application code |
| `ENV PYTHONUNBUFFERED=1` | Don't buffer Python output |
| `EXPOSE 8000` | Document which port is used |
| `CMD ["uvicorn", ...]` | Command to run API when container starts |

### Important Note

The `--host 0.0.0.0` is crucial! Without it, the API won't be accessible from outside the container.

---

## Step 3: Create .dockerignore

Like `.gitignore`, this file tells Docker which files to skip when building the image.

Create `.dockerignore` in chapter7/ directory:

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

This keeps the image smaller by excluding unnecessary files.

---

## Step 4: Start Docker Desktop

Open Docker Desktop application on your machine. You'll see it starting up in the background. Wait until you see:

```
Docker Desktop is running ✓
```

The Docker daemon needs to be running before you can build images.

---

## Step 5: Build Docker Image

### Build Command

In your terminal, navigate to `FastAPI_Course/chapter7/` directory:

```bash
cd /path/to/FastAPI_Course/chapter7

# Build the image
docker build -t your-username/insurance-api:1.0 .
```

Replace `your-username` with your actual Docker Hub username!

### What Happens

```
Step 1/9 : FROM python:3.9-slim
 ---> Downloaded base image

Step 2/9 : WORKDIR /app
 ---> Created working directory

Step 3/9 : COPY requirements.txt .
 ---> Copied requirements file

Step 4/9 : RUN pip install...
 ---> Installing packages (might take 1-2 minutes)

Step 5/9 : COPY . .
 ---> Copied application code

Step 6/9 : ENV PYTHONUNBUFFERED=1
 ---> Set environment

Step 7/9 : EXPOSE 8000
 ---> Documented port

Step 8/9 : CMD ["uvicorn", ...]
 ---> Set startup command

Step 9/9 : Successfully built abc123def456
```

### Expected Output

```
Successfully built abc123def456
Successfully tagged your-username/insurance-api:1.0
```

### Verify Image Was Built

**Option 1: Using Docker Desktop**
- Open Docker Desktop
- Go to "Images" tab
- Look for your image: `your-username/insurance-api:1.0`

**Option 2: Using Command Line**
```bash
docker images
# Should show your-username/insurance-api in the list
```

---

## Step 6: Test Locally Before Publishing

### Run Container Locally

```bash
docker run -d -p 8000:8000 --name insurance-api your-username/insurance-api:1.0
```

**Flags explained:**
- `-d` = Run in detached mode (background)
- `-p 8000:8000` = Map host port 8000 to container port 8000
- `--name insurance-api` = Give container a friendly name

### Test the API

Open your browser and visit:

```
http://localhost:8000
```

You should see the home endpoint response:
```json
{
  "message": "Insurance Premium Prediction API",
  "version": "1.0",
  "endpoints": [
    "/",
    "/health",
    "/predict",
    "/docs"
  ]
}
```

### Test Swagger Docs

Visit: http://localhost:8000/docs

You should see the interactive API documentation where you can test the predict endpoint.

### Test Health Check

Visit: http://localhost:8000/health

```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "RandomForest v1.0"
}
```

### Stop Container

```bash
docker stop insurance-api
docker rm insurance-api
```

---

## Step 7: Login to Docker Hub

Before pushing to Docker Hub, authenticate with your credentials:

```bash
docker login
```

You'll be prompted for:
- Username: Your Docker Hub username
- Password: Your Docker Hub password

If successful:
```
Login Succeeded
```

---

## Step 8: Push Image to Docker Hub

Upload your image to Docker Hub:

```bash
docker push your-username/insurance-api:1.0
```

### What Happens

Docker compresses and uploads each layer:

```
The push refers to repository [docker.io/your-username/insurance-api]
abc123: Pushed
def456: Pushed
ghi789: Pushed
...
1.0: digest: sha256:abc123... size: 2048
```

This might take 2-5 minutes depending on image size and internet speed.

### Verify on Docker Hub

1. Go to https://hub.docker.com
2. Login to your account
3. Look for `insurance-api` in your repositories
4. You should see tag `1.0` listed

---

## Step 9: Simulate Being a Different User (Tester)

Now let's simulate a scenario where a tester (on a different machine with clean Docker) gets your image.

### Clean Local Docker

First, let's remove the image from our local machine to simulate a fresh state:

```bash
# List images
docker images

# Remove your image
docker rmi your-username/insurance-api:1.0

# Verify it's gone
docker images | grep insurance-api
# (Should show nothing)
```

### Pull from Docker Hub

Now pull the image from Docker Hub as if you're a fresh user:

```bash
docker pull your-username/insurance-api:1.0
```

Output:
```
1.0: Pulling from your-username/insurance-api
abc123: Pull complete
def456: Pull complete
...
Status: Downloaded newer image for your-username/insurance-api:1.0
```

### Run the Pulled Image

```bash
docker run -d -p 8000:8000 --name insurance-api-test your-username/insurance-api:1.0
```

### Test It Works

Visit: http://localhost:8000/docs

Test the predict endpoint with sample data:

```json
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

Expected response:
```json
{
  "predicted_category": "High",
  "confidence": 0.95,
  "class_probabilities": {
    "High": 0.95,
    "Medium": 0.04,
    "Low": 0.01
  }
}
```

**This proves the image works identically on different machines!** ✅

---

## File Structure After Dockerization

```
FastAPI_Course/chapter7/
├── main.py
├── requirements.txt
├── Dockerfile                    ← NEW
├── .dockerignore                 ← NEW
├── schemas/
│   ├── user_input.py
│   └── prediction_response.py
├── config/
│   └── city_tier.py
├── models/
│   ├── predict.py
│   └── model.pkl
├── chapter7.md
└── README.md
```

---

## Common Issues & Solutions

### Issue 1: "Docker daemon not running"

**Solution:** Start Docker Desktop

### Issue 2: "Port 8000 already in use"

**Solution:** Use different port
```bash
docker run -d -p 8001:8000 your-username/insurance-api:1.0
```

### Issue 3: "Login failed to Docker Hub"

**Solution:** Check your credentials
```bash
docker logout
docker login
```

### Issue 4: "Image build failed"

**Common causes:**
- Missing requirements.txt
- Missing model.pkl file
- Incorrect Python version

**Solution:** Check all files are in chapter7/ directory

### Issue 5: "Container exits immediately"

**Solution:** Check logs
```bash
docker logs container_id
```

---

## Key Takeaways

✅ **Dockerfile defines how to build your image**
- Base image selection
- Dependency installation
- Code copying
- Port exposure
- Startup command

✅ **Docker image is a package containing everything**
- Application code
- Dependencies
- Python runtime
- Model file
- Configuration

✅ **Docker container is a running instance**
- Image → Blueprint
- Container → Running process

✅ **Docker Hub enables sharing**
- Push your image
- Others can pull and run
- Works on any machine

✅ **Consistency across environments**
- Dev machine ✓
- Tester machine ✓
- Production server ✓

---

## Benefits Realized

### For Developers
- ✅ No more "it works on my machine" excuses
- ✅ Easy to share with teammates
- ✅ Consistent environment every time

### For Testers
- ✅ Easy to get and run the application
- ✅ No setup needed - just run the image
- ✅ Test exactly what will go to production

### For DevOps/Production
- ✅ Predictable deployment
- ✅ Easy scaling
- ✅ Quick rollback if needed

---

## Docker Image Versioning

### Tag Your Images Properly

When you build, use semantic versioning:

```bash
# Version 1.0 - Initial release
docker build -t your-username/insurance-api:1.0 .

# Version 1.1 - Bug fix
docker build -t your-username/insurance-api:1.1 .

# Latest version (always points to latest)
docker build -t your-username/insurance-api:latest .

# Push all versions
docker push your-username/insurance-api:1.0
docker push your-username/insurance-api:1.1
docker push your-username/insurance-api:latest
```

---

## What's Next?

### Chapter 9 Preview: AWS Deployment

In the next chapter, we'll take this Docker image and deploy it to AWS, making it accessible to everyone on the internet!

```
Your Docker Image
       ↓
   AWS ECR
       ↓
  AWS ECS
       ↓
  Load Balancer
       ↓
  https://your-api.com/predict (Publicly accessible!)
```

---

## Summary

| Step | Action | Command |
|------|--------|---------|
| 1 | Create Dockerfile | Write Dockerfile (see Step 2) |
| 2 | Build image | `docker build -t username/insurance-api:1.0 .` |
| 3 | Test locally | `docker run -p 8000:8000 ...` |
| 4 | Login to Hub | `docker login` |
| 5 | Push to Hub | `docker push username/insurance-api:1.0` |
| 6 | Pull from Hub | `docker pull username/insurance-api:1.0` |
| 7 | Run anywhere | `docker run -p 8000:8000 ...` |

---

## Hands-On Exercises

### Exercise 1: Build and Test Locally (10 min)
1. Create Dockerfile in your chapter7 directory
2. Build the image
3. Run it locally
4. Test all endpoints in Swagger
5. Stop the container

### Exercise 2: Push to Docker Hub (10 min)
1. Login to Docker Hub
2. Push your image
3. Verify on Docker Hub website
4. Share the link with someone

### Exercise 3: Pull as New User (10 min)
1. Delete the local image
2. Pull from Docker Hub
3. Run the pulled image
4. Verify it works identically

### Exercise 4: Try Different Port (5 min)
1. Run same image on port 8001
2. Verify it works at http://localhost:8001
3. Run two instances simultaneously
4. Verify both work independently

---

## Interview Questions

**Q1: Why do we use Docker?**
A: To ensure applications run identically across dev, test, and production environments.

**Q2: What's the difference between image and container?**
A: Image is a blueprint (static), container is a running instance (dynamic).

**Q3: Why is `--host 0.0.0.0` important?**
A: It makes the API accessible from outside the container (from host machine).

**Q4: What does `docker push` do?**
A: Uploads your local image to Docker Hub registry.

**Q5: How can a tester get your application?**
A: They simply pull your image from Docker Hub and run it.

---

## Next Steps

✅ Complete this chapter  
✅ Docker image running locally  
✅ Image pushed to Docker Hub  
→ Continue to Chapter 9: AWS Deployment (Coming next!)

---

**Estimated Time:** 30-40 minutes  
**Difficulty:** Intermediate (requires Docker basics)  
**Hands-on:** Yes, complete exercises recommended
