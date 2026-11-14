# Chapter 9: AWS EC2 Deployment

**Quick Start:** Deploy your Dockerized FastAPI API to AWS and make it publicly accessible

## 🎯 What You'll Learn

- Launch AWS EC2 instances
- Install and configure Docker on EC2
- Deploy your Docker image from Docker Hub
- Configure security groups for public access
- Access your API from anywhere on internet
- Build a Streamlit frontend to interact with deployed API

## 📋 Prerequisites

- ✅ Completed Chapter 8 (Docker image pushed to Docker Hub)
- ✅ AWS Account (free tier eligible)
- ✅ Basic understanding of cloud services
- ✅ Docker image accessible on Docker Hub

## ⏱️ Time Required

- **Setup:** 15-20 minutes
- **Deployment:** 20-30 minutes
- **Testing:** 10-15 minutes
- **Total:** 45-60 minutes

## 🚀 Quick Start (5 Steps)

### Step 1: Create AWS Account
- Visit https://aws.amazon.com
- Sign up (free tier available)
- Verify email and payment method

### Step 2: Launch EC2 Instance
- Search "EC2" in AWS console
- Click "Instances" → "Launch Instance"
- **Configuration:**
  - Name: `MyFastAPIServer`
  - OS: Ubuntu Server 22.04 LTS
  - Type: **t2.micro** (FREE! ✅)
  - Key Pair: Create or select existing
  - Security: Allow SSH
- Click "Launch"

### Step 3: Connect to EC2
- Click "Connect" button (browser terminal)
- Or use SSH with key pair

### Step 4: Setup Docker
```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
exit  # Reconnect
```

### Step 5: Pull and Run Your Image
```bash
# Pull from Docker Hub
docker pull YOUR_USERNAME/insurance-api:1.0

# Run the container
docker run -d -p 8000:8000 YOUR_USERNAME/insurance-api:1.0

# Verify it's running
docker ps
```

### Step 6: Configure Security Group
1. Go to EC2 Instances
2. Select your instance → Security tab
3. Click Security Group
4. Edit inbound rules
5. Add rule:
   - Type: Custom TCP
   - Port: 8000
   - Source: 0.0.0.0/0
6. Save

### Step 7: Access Your API
```
http://YOUR_PUBLIC_IP:8000
http://YOUR_PUBLIC_IP:8000/docs
```

Test with the Swagger UI documentation!

---

## 📊 Architecture

```
Your Docker Image (Docker Hub)
         ↓
    Pull on EC2
         ↓
   AWS EC2 Instance
   (Ubuntu + Docker)
         ↓
   FastAPI Container
   (Port 8000)
         ↓
  Public IP Address
         ↓
 Accessible on Internet!
```

---

## 🔧 Commands Reference

### EC2 Connection
```bash
# SSH into instance
ssh -i api-aws-key.pem ubuntu@YOUR_PUBLIC_IP

# Or use browser terminal (easier)
```

### Docker Operations
```bash
# Pull image
docker pull YOUR_USERNAME/insurance-api:1.0

# Run container
docker run -d -p 8000:8000 YOUR_USERNAME/insurance-api:1.0

# View running containers
docker ps

# View logs
docker logs container_id
docker logs -f container_id  # Follow

# Stop container
docker stop container_id

# Restart container
docker restart container_id
```

### Verify Deployment
```bash
# Check Docker is running
docker ps

# Check logs for errors
docker logs container_id

# Test API locally on EC2
curl http://localhost:8000/health
```

---

## 🌐 Streamlit Frontend

### Create Local Streamlit App

File: `app.py`
```python
import streamlit as st
import requests

st.title("🏥 Insurance Premium Prediction")

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", 18, 100, 30)
    weight = st.number_input("Weight (kg)", 30, 150, 70)
    height = st.number_input("Height (m)", 1.0, 2.5, 1.70)
with col2:
    income = st.number_input("Income (LPA)", 1, 100, 10)
    smoker = st.checkbox("Smoker?")
    city = st.selectbox("City", ["delhi", "mumbai", "bangalore", "gurgaon", "pune"])

# IMPORTANT: Replace with your AWS IP
API_BASE_URL = "http://YOUR_AWS_IP:8000"

if st.button("🔮 Predict Premium"):
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json={
                "age": int(age),
                "weight": float(weight),
                "height": float(height),
                "income_lpa": int(income),
                "smoker": smoker,
                "city": city,
                "occupation": "employed"
            }
        )
        if response.status_code == 200:
            result = response.json()
            st.success(f"Premium: {result['predicted_category']}")
            st.metric("Confidence", f"{result['confidence']:.2%}")
        else:
            st.error(f"Error: {response.status_code}")
    except Exception as e:
        st.error(f"Cannot reach API: {str(e)}")
```

### Run Streamlit
```bash
pip install streamlit requests
streamlit run app.py
```

Visit: `http://localhost:8501`

---

## 🆓 Free Tier Benefits

| Resource | Quota | Duration |
|----------|-------|----------|
| EC2 t2.micro | 750 hours/month | 12 months |
| Data Out | 15 GB/month | 12 months |
| Storage | 5 GB S3 | 12 months |

**750 hours = 24/7 for ~25 days** ✅

---

## ⚠️ Common Issues

| Problem | Solution |
|---------|----------|
| Can't access API | Check security group allows port 8000 |
| Connection refused | Verify container is running: `docker ps` |
| API returns error | Check logs: `docker logs container_id` |
| Container exits | View logs for error details |
| Can't SSH to EC2 | Use browser-based terminal instead |
| Port already in use | Use different port: `docker run -p 8001:8000` |

---

## 🔒 Security Checklist

- ✅ Security group only allows needed ports
- ✅ SSH from your IP (not 0.0.0.0/0)
- ✅ Keep key pair (.pem) file secure
- ✅ Never commit key to Git
- ✅ Use strong passwords
- ✅ Keep Docker updated

---

## 💰 Cost Estimation

### Free Tier (First 12 Months)
```
t2.micro:        $0
Data transfer:   $0 (within 15GB/month)
Storage:         $0 (within 5GB)
Total:           $0 ✅
```

### After Free Tier
```
t2.micro:        ~$7-10/month
Data transfer:   $0.09/GB over 15GB
Total:           ~$10-15/month
```

---

## 📋 Verification Checklist

After deployment, verify:

- [ ] AWS account created
- [ ] EC2 instance launched (t2.micro)
- [ ] Connected to EC2 successfully
- [ ] Docker installed on EC2
- [ ] Docker image pulled successfully
- [ ] Container running (`docker ps`)
- [ ] Security group allows port 8000
- [ ] Can access home endpoint via browser
- [ ] Can access /health endpoint
- [ ] Can access /docs (Swagger UI)
- [ ] Can test /predict endpoint
- [ ] Streamlit frontend working locally
- [ ] Streamlit connects to deployed API
- [ ] All predictions working end-to-end

---

## 🎓 Hands-On Exercises

### Exercise 1: Deploy API (30 min)
1. Launch EC2 instance
2. Install Docker
3. Pull your image
4. Run container
5. Configure security group
6. Verify access from browser
7. Document public IP

### Exercise 2: Streamlit Integration (15 min)
1. Create Streamlit app
2. Replace API URL with your AWS IP
3. Test all endpoints
4. Verify predictions work

### Exercise 3: Monitoring (10 min)
1. View container logs
2. Check running containers
3. Monitor resource usage
4. Test error handling

### Exercise 4: Scaling Preparation (10 min)
1. Research AWS ECS
2. Compare EC2 vs ECS vs Kubernetes
3. Plan next steps for production

---

## 🌟 Learning Path Completion

```
Chapter 1-6: API Fundamentals
     ✅ Completed

Chapter 7: Production Improvements
     ✅ Completed

Chapter 8: Dockerization
     ✅ Completed

Chapter 9: Cloud Deployment ← You are here! 🎉
     ✅ Completed

Result: Professional ML API deployed globally! 🌍
```

---

## 📚 Related Resources

### Docker_Course
- See **1-fundamentals/** for Docker concepts
- See **2-practical/** for Docker best practices
- See **4-deployment/** for advanced deployment strategies

### Next Topics
- **Kubernetes:** Container orchestration at scale
- **CI/CD:** Automate deployment pipeline
- **Load Balancing:** Distribute traffic
- **HTTPS:** Secure your API
- **Auto Scaling:** Handle traffic spikes

---

## 🎯 What's Next?

After this chapter, you can:

✅ Deploy any Docker application to AWS  
✅ Make applications globally accessible  
✅ Build scalable systems  
✅ Implement monitoring  
✅ Plan for production deployments  

### Advanced Topics (Future Learning)
- AWS ECS (container orchestration)
- RDS (managed databases)
- S3 (object storage)
- Lambda (serverless)
- CloudFront (CDN)

---

## 💡 Key Takeaways

1. **EC2 provides always-on computing** - Your laptop isn't always on, but EC2 is
2. **Docker ensures consistency** - Same image runs identically everywhere
3. **Public IP enables global access** - Anyone can reach your API
4. **Security groups control traffic** - Firewall rules for safety
5. **Free tier is generous** - Enough for learning and small projects

---

## 🎓 Interview Questions

**Q: Why would you use EC2 instead of a laptop?**  
A: Always on, globally accessible, reliable, scalable, and professional infrastructure.

**Q: How does your API reach the internet?**  
A: EC2 instance has a public IP address that's routable from internet.

**Q: What if EC2 stops unexpectedly?**  
A: systemctl enable docker ensures Docker restarts automatically.

**Q: How would you handle 10,000 users?**  
A: Use load balancer + multiple EC2 instances, or move to ECS/Kubernetes.

**Q: How is this different from Heroku?**  
A: AWS gives more control; Heroku is simpler but less flexible and more expensive.

---

**Time to Complete:** 45-60 minutes  
**Difficulty:** Intermediate  
**Hands-on Requirement:** Yes (Deploy and test)  
**Final Checkpoint:** API accessible globally via public IP ✅

---

## 📖 Full Guide

See **[chapter9.md](./chapter9.md)** for complete detailed guide with:
- Step-by-step AWS setup
- Deep explanations
- Streamlit code examples
- Troubleshooting guide
- Security best practices
- Scaling strategies

---

🚀 **Congratulations!** You've completed the entire FastAPI journey from basics to cloud deployment!
