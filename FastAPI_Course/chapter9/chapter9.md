# Chapter 9: AWS EC2 Deployment

## Overview

In this final chapter, we'll take the Dockerized FastAPI application from Chapter 8 and deploy it to AWS EC2, making it publicly accessible on the internet.

**Prerequisites:**
- Completed Chapter 8 (Dockerized API)
- Docker image pushed to Docker Hub
- AWS Account (free tier eligible)
- Basic understanding of cloud services

**Time to complete:** 45-60 minutes

---

## Learning Objectives

By the end of this chapter, you'll be able to:

✅ Create and configure an AWS EC2 instance  
✅ Install Docker on EC2  
✅ Pull and run your Docker image on EC2  
✅ Configure security groups for external access  
✅ Access your API from anywhere on the internet  
✅ Connect a Streamlit frontend to your deployed API  
✅ Monitor and troubleshoot your deployment  

---

## Why AWS EC2?

### The Journey So Far

```
Chapter 1-6: Build the API locally
Chapter 7: Improve with production patterns
Chapter 8: Containerize with Docker
Chapter 9: Deploy to the cloud ← You are here
    ↓
Result: Public API accessible to the world! 🌍
```

### Benefits of Cloud Deployment

| Local Machine | AWS EC2 |
|---------------|---------|
| ❌ Only works when your laptop is on | ✅ Always running 24/7 |
| ❌ Needs your personal IP | ✅ Public IP address |
| ❌ Limited by your internet | ✅ Enterprise-grade bandwidth |
| ❌ Can't handle many users | ✅ Can scale to millions |
| ❌ No backup/recovery | ✅ Built-in redundancy |

---

## Architecture Overview

```
Your Laptop → Docker Image → Docker Hub
                              ↓
                          AWS EC2 Instance
                              ↓
                         Running Container
                              ↓
                        Public IP (e.g., 54.1.2.3)
                              ↓
                    Internet (Anyone can access)
```

---

## Step 1: Create AWS Account

### 1.1 Sign Up

1. Go to https://aws.amazon.com
2. Click "Create an AWS Account"
3. Fill in email, password, and account details
4. Verify your email address
5. Add payment method (won't be charged for free tier)
6. Complete identity verification

### 1.2 Login to AWS Console

1. Visit https://console.aws.amazon.com
2. Sign in with your credentials
3. You should see the AWS Management Console

### 1.3 Free Tier Benefits

As a new account, you get:
- **EC2:** 750 hours/month of t2.micro instances (enough for always-on service)
- **Data Transfer:** 15 GB outbound/month
- **Storage:** 5 GB S3 storage

✅ **This is completely free for 1 year!**

---

## Step 2: Launch EC2 Instance

### 2.1 Navigate to EC2

1. In AWS Console, search for "EC2"
2. Click on "Elastic Compute Cloud (EC2)"
3. Click "Instances" in the left sidebar
4. Click "Launch Instance" button

### 2.2 Configure Instance

**Instance Name:**
```
MyFastAPIServer
```

**Amazon Machine Image (AMI):**
- Select "Ubuntu Server 22.04 LTS"
- Architecture: 64-bit (x86)

**Instance Type:**
```
t2.micro (Free tier eligible)
- 1 vCPU
- 1 GB Memory
```

⚠️ **IMPORTANT:** Always use t2.micro to stay within free tier!

**Key Pair:**
- Create new key pair or select existing
- Name: `api-aws-key`
- Format: `.pem` (for Linux/macOS) or `.ppk` (for Windows)
- ✅ Save this file securely - you'll need it for SSH access

**Network Settings:**

Allow SSH traffic:
```
✅ Allow SSH traffic from Anywhere
   (or specify your IP for security)
```

**Storage:**
```
Root volume: 8 GB gp2 (General Purpose)
```

### 2.3 Launch

Click "Launch Instance" button and wait for:
```
Instance State: running ✓
Instance ID: i-xxxxxxxxx
Public IPv4: 54.xxx.xxx.xxx
```

---

## Step 3: Connect to EC2 Instance

### 3.1 Get Connection Information

1. Go to Instances list
2. Select your instance
3. Click "Connect" button
4. Use the browser-based terminal OR
5. Use SSH from your local terminal

### 3.2 Browser Terminal (Easiest)

1. Click "Connect" button
2. Tab: "EC2 Instance Connect"
3. Click "Connect"
4. A terminal window opens
5. You're now connected to your EC2 instance!

### 3.3 SSH Terminal (Alternative)

```bash
# Download your key pair and navigate to its location
chmod 400 api-aws-key.pem

# Connect via SSH
ssh -i api-aws-key.pem ubuntu@YOUR_PUBLIC_IP
# Example: ssh -i api-aws-key.pem ubuntu@54.123.45.67
```

---

## Step 4: Install and Setup Docker

### 4.1 Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### 4.2 Install Docker

```bash
# Install Docker
sudo apt install -y docker.io

# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Add ubuntu user to docker group (avoid using sudo)
sudo usermod -aG docker ubuntu

# Verify Docker installation
docker --version
```

### 4.3 Grant Permissions

```bash
# Exit current connection
exit

# Reconnect (to apply group changes)
# Use browser terminal or SSH again
```

---

## Step 5: Pull Docker Image from Docker Hub

### 5.1 Pull Your Image

```bash
# Pull your image from Docker Hub
docker pull YOUR_USERNAME/insurance-api:1.0

# Verify image is downloaded
docker images
```

Example output:
```
REPOSITORY                    TAG    IMAGE ID
your-username/insurance-api   1.0    abc123def456
```

### 5.2 Test Image Locally

```bash
# Run container
docker run -d -p 8000:8000 YOUR_USERNAME/insurance-api:1.0

# Verify container is running
docker ps
```

---

## Step 6: Configure Security Group

### 6.1 Problem

Even though your API is running on EC2, you can't access it from the internet because the security group blocks traffic on port 8000.

### 6.2 Solution: Edit Security Group

1. Go to EC2 Instances
2. Select your instance
3. Click "Security" tab
4. Click on Security Group link
5. Click "Edit inbound rules"

### 6.3 Add Rule for Port 8000

Click "Add rule":
- **Type:** Custom TCP
- **Port Range:** 8000
- **Source:** 0.0.0.0/0 (Anyone from internet)
- Click "Save rules"

Result:
```
Protocol    Port Range    Source
TCP         8000          0.0.0.0/0
SSH         22            Your IP (for management)
HTTP        80            0.0.0.0/0 (optional)
HTTPS       443           0.0.0.0/0 (optional)
```

---

## Step 7: Access Your API

### 7.1 Get Public IP

1. Go to Instances
2. Select your instance
3. Copy "Public IPv4" address
   Example: `54.123.45.67`

### 7.2 Test API Endpoints

**Home Endpoint:**
```
http://54.123.45.67:8000
```

**Health Check:**
```
http://54.123.45.67:8000/health
```

**API Documentation:**
```
http://54.123.45.67:8000/docs
```

Test with Swagger UI:
- Scroll to `/predict` endpoint
- Click "Try it out"
- Fill in sample data:
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
- Click "Execute"
- You should get prediction results!

---

## Step 8: Create Streamlit Frontend

### 8.1 Create Streamlit Application

Create file `app.py` on your local machine:

```python
import streamlit as st
import requests
import json

# Configure page
st.set_page_config(
    page_title="Insurance Premium Predictor",
    layout="centered"
)

# Title
st.title("🏥 Insurance Premium Prediction")
st.markdown("Predict insurance premium based on personal details")

# API Configuration
API_BASE_URL = "http://YOUR_AWS_IP:8000"  # Replace with your AWS IP

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    weight = st.number_input("Weight (kg)", min_value=30, max_value=150, value=70)
    height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01)

with col2:
    income = st.number_input("Annual Income (LPA)", min_value=1, max_value=100, value=10)
    smoker = st.checkbox("Smoker?", value=False)
    city = st.selectbox("City", ["delhi", "mumbai", "bangalore", "gurgaon", "pune"])

occupation = st.selectbox("Occupation", ["student", "employed", "self-employed", "retired"])

# Predict button
if st.button("🔮 Predict Premium", use_container_width=True):
    try:
        # Prepare request data
        data = {
            "age": int(age),
            "weight": float(weight),
            "height": float(height),
            "income_lpa": int(income),
            "smoker": smoker,
            "city": city,
            "occupation": occupation
        }
        
        # Make API call
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Display results
            st.success("✅ Prediction successful!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Premium Category", result["predicted_category"])
            with col2:
                st.metric("Confidence", f"{result['confidence']:.2%}")
            with col3:
                st.metric("Risk Level", 
                         "🟢 Low" if result["predicted_category"] == "Low" 
                         else "🟡 Medium" if result["predicted_category"] == "Medium"
                         else "🔴 High")
            
            # Show detailed probabilities
            st.subheader("Class Probabilities")
            probabilities = result["class_probabilities"]
            
            cols = st.columns(3)
            for idx, (category, prob) in enumerate(probabilities.items()):
                with cols[idx]:
                    st.progress(prob, text=f"{category}: {prob:.1%}")
        
        else:
            st.error(f"❌ Error: {response.status_code}")
            st.error(response.text)
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to API. Check:")
        st.error("1. AWS IP address is correct")
        st.error("2. EC2 instance is running")
        st.error("3. Security group allows port 8000")
        st.error("4. API container is running")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Display API Status
st.divider()
col1, col2 = st.columns(2)

with col1:
    if st.button("Check API Health", use_container_width=True):
        try:
            health = requests.get(f"{API_BASE_URL}/health", timeout=2)
            if health.status_code == 200:
                st.success("✅ API is healthy!")
                st.json(health.json())
            else:
                st.error(f"API returned status: {health.status_code}")
        except Exception as e:
            st.error(f"❌ Cannot reach API: {str(e)}")

with col2:
    if st.button("View API Docs", use_container_width=True):
        st.markdown(f"[🔗 Open Swagger UI]({API_BASE_URL}/docs)", unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
### How it Works
1. Enter your personal details
2. Click "Predict Premium"
3. AI model predicts your insurance premium category
4. Confidence score shows model certainty

**Powered by:** FastAPI + Machine Learning + AWS EC2
""")
```

### 8.2 Install Streamlit

```bash
pip install streamlit requests
```

### 8.3 Update API URL

In `app.py`, replace `YOUR_AWS_IP` with your actual AWS public IP:
```python
API_BASE_URL = "http://54.123.45.67:8000"
```

### 8.4 Run Streamlit

```bash
streamlit run app.py
```

Streamlit will open at `http://localhost:8501`

---

## Step 9: Complete Workflow

### 9.1 Development to Production Pipeline

```
1. LOCAL DEVELOPMENT
   └─ Write Python code
   └─ Test locally with FastAPI
   └─ Test with Streamlit frontend

2. CONTAINERIZATION (Chapter 8)
   └─ Create Dockerfile
   └─ Build Docker image
   └─ Test Docker image locally
   └─ Push to Docker Hub

3. CLOUD DEPLOYMENT (Chapter 9)
   └─ Create EC2 instance
   └─ Install Docker on EC2
   └─ Pull image from Docker Hub
   └─ Run container on EC2
   └─ Configure security groups
   └─ Access via public IP
   └─ Update frontend to use public IP
   └─ API now accessible globally! 🌍
```

### 9.2 Architectural Diagram

```
                    Internet Users (Anyone)
                              ↓
                    http://54.123.45.67:8000
                              ↓
                     AWS EC2 Instance
                     ┌──────────────┐
                     │   Ubuntu OS  │
                     ├──────────────┤
                     │    Docker    │
                     ├──────────────┤
                     │  FastAPI App │
                     │   (Port 8000)│
                     ├──────────────┤
                     │  ML Model    │
                     │ (Insurance)  │
                     └──────────────┘
                              ↑
                        Public IP visible
                        to the internet
```

---

## Step 10: Monitoring and Maintenance

### 10.1 View Running Container

```bash
# SSH into your EC2 instance
ssh -i api-aws-key.pem ubuntu@YOUR_PUBLIC_IP

# View running containers
docker ps

# View logs
docker logs container_id
docker logs -f container_id  # Follow logs

# View resource usage
docker stats
```

### 10.2 Restart Container

```bash
# Stop container
docker stop container_id

# Start container again
docker start container_id

# Or remove and re-run
docker rm container_id
docker run -d -p 8000:8000 YOUR_USERNAME/insurance-api:1.0
```

### 10.3 Stop EC2 Instance

To save costs (when not using):
1. Go to Instances
2. Right-click instance
3. Select "Instance State" → "Stop"

To restart:
1. Right-click instance
2. Select "Instance State" → "Start"

⚠️ **Note:** Public IP may change after stopping and restarting!

---

## Common Issues & Troubleshooting

### Issue 1: Can't Connect to API

**Symptoms:** `Connection refused` or timeout

**Solutions:**
```bash
# Check if container is running
docker ps

# Check security group allows port 8000
# (Go to AWS Console → Security Groups)

# Check if container is listening on 0.0.0.0
docker logs container_id

# Verify public IP is correct
# Go to Instances → Public IPv4 address
```

### Issue 2: API Returns Error 502

**Symptoms:** `Bad Gateway` error

**Solutions:**
```bash
# Check Docker is running
docker ps

# Check container logs
docker logs container_id

# Restart container
docker restart container_id
```

### Issue 3: Port Already in Use

**Symptoms:** `Address already in use`

**Solutions:**
```bash
# Find what's using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 PID

# Or use different port
docker run -d -p 8001:8000 YOUR_USERNAME/insurance-api:1.0
# Then update security group to allow 8001
```

### Issue 4: Can't SSH into EC2

**Symptoms:** `Connection timeout`

**Solutions:**
- Use browser-based terminal instead
- Verify security group allows SSH on port 22
- Verify key pair is correct

### Issue 5: Out of Free Tier Quota

**Solutions:**
- Monitor EC2 usage in AWS Billing console
- Stop unused instances
- Set up billing alerts

---

## Cost Optimization

### Free Tier Limits

```
EC2 t2.micro:        750 hours/month (24/7 for ~25 days)
Data Transfer Out:   15 GB/month
Free Tier Eligible:  12 months
```

### Optimize Usage

1. Use t2.micro instance type
2. Stop instance when not needed
3. Monitor data transfer
4. Set up AWS billing alerts

### Estimate Monthly Cost (Beyond Free Tier)

- t2.micro: ~$7-10/month
- Data transfer: ~$0.09 per GB
- Storage: ~$0.10 per GB

---

## Security Best Practices

### 1. Security Groups

❌ **Don't do this:**
```
Protocol: All
Port: All
Source: 0.0.0.0/0
```

✅ **Do this:**
```
SSH (22):     Your IP only
HTTP (80):    0.0.0.0/0 (optional)
Custom (8000): 0.0.0.0/0 (your API)
```

### 2. Key Management

- Store `.pem` file securely
- Never commit to Git
- Use strong passwords
- Rotate credentials regularly

### 3. API Security

- Add authentication later
- Use HTTPS (SSL/TLS) in production
- Implement rate limiting
- Add input validation (already done in Chapter 7!)

### 4. Regular Updates

```bash
# Keep system updated
sudo apt update
sudo apt upgrade -y

# Keep Docker updated
sudo apt upgrade docker.io -y
```

---

## Next Steps

### Scale Your Application

Once basic deployment works, consider:

1. **Load Balancing**
   - AWS ELB for multiple instances
   - Distribute traffic automatically

2. **Auto Scaling**
   - Automatically spin up instances based on demand
   - Save costs by scaling down

3. **Database**
   - Add AWS RDS for persistent data
   - Store predictions in database

4. **HTTPS**
   - Get SSL certificate
   - Enable HTTPS on your API

5. **CI/CD Pipeline**
   - Automate deployment
   - GitHub Actions → Docker Build → ECR → ECS

6. **Container Orchestration**
   - Use AWS ECS or Kubernetes
   - Manage multiple containers easily

---

## File Structure After Deployment

```
FastAPI_Course/chapter9/
├── chapter9.md                          (This file)
├── README.md                            (Quick start)
├── streamlit_app.py                     (Frontend)
├── deployment_checklist.md              (Verification steps)
├── aws_troubleshooting.md               (Common issues)
└── backend_api_url.txt                  (Your AWS IP)
```

---

## Summary

| Step | Action | Time |
|------|--------|------|
| 1 | Create AWS account | 5 min |
| 2 | Launch EC2 instance | 5 min |
| 3 | Connect to instance | 2 min |
| 4 | Install Docker | 5 min |
| 5 | Pull Docker image | 5 min |
| 6 | Configure security group | 5 min |
| 7 | Access API | 2 min |
| 8 | Create Streamlit frontend | 10 min |
| 9 | Test everything | 10 min |

**Total Time:** 45-60 minutes

---

## Hands-On Exercises

### Exercise 1: Deploy Your API (30 min)
1. Create AWS account
2. Launch EC2 instance
3. Connect and setup Docker
4. Pull your Docker image
5. Verify API is accessible
6. Document the public IP

### Exercise 2: Frontend Integration (15 min)
1. Create Streamlit app locally
2. Update API URL to your AWS IP
3. Test all prediction endpoints
4. Verify health check works

### Exercise 3: Monitoring (10 min)
1. Check running containers
2. View Docker logs
3. Check CPU/memory usage
4. Test API during traffic

### Exercise 4: Troubleshooting (15 min)
1. Intentionally stop container
2. Verify API returns error
3. Restart container
4. Verify recovery

---

## Interview Questions

**Q1: Why use EC2 instead of running on laptop?**
A: EC2 is always on, has public IP, better bandwidth, and can handle more users.

**Q2: What if EC2 stops and restarts?**
A: The systemctl enable docker command ensures Docker starts automatically.

**Q3: Why configure security groups?**
A: They act as firewall rules - without them, external traffic can't reach port 8000.

**Q4: How much does this cost?**
A: Free for first 12 months (750 hours/month of t2.micro), then ~$7-10/month.

**Q5: What if I need to scale to 1000 users?**
A: Use multiple EC2 instances + load balancer, or move to AWS ECS/Kubernetes.

---

## 🤔 Confusing Questions (Follow-Up Interview Questions)

### Q6: What's the difference between public and private IP? Can you SSH with private IP?

**Answer:**

Public IP is internet-facing, private IP is internal:

```
Private IP (e.g., 10.0.0.5):
  - Only accessible within AWS network
  - EC2 ↔ EC2 communication
  - RDS database ↔ EC2
  - NOT accessible from internet

Public IP (e.g., 203.45.67.89):
  - Accessible from anywhere on internet
  - Your laptop can SSH using this
  - Client requests come to this

Public DNS (e.g., ec2-203-45-67-89.compute-1.amazonaws.com):
  - Human-readable version of public IP
  - Same as public IP, just different format
```

**SSH from laptop:**

```bash
# ✅ Works (public IP)
ssh -i key.pem ubuntu@203.45.67.89

# ✅ Works (public DNS)
ssh -i key.pem ubuntu@ec2-203-45-67-89.compute-1.amazonaws.com

# ❌ Fails (private IP from outside AWS)
ssh -i key.pem ubuntu@10.0.0.5
# Can't reach private IP from internet!
```

**Private IP only works inside AWS:**

```bash
# ✅ Works (EC2 to EC2 on private IP)
ssh -i key.pem ubuntu@10.0.0.5  # From another EC2

# ❌ Fails (From laptop on private IP)
ssh -i key.pem ubuntu@10.0.0.5  # Can't reach from internet
```

---

### Q7: If EC2 is stopped, does it still cost money?

**Answer:**

PARTIALLY! Storage still costs:

```
Running EC2 (t2.micro):
  - Compute: Free (first 12 months)
  - Storage: $0.10/GB/month

Stopped EC2:
  - Compute: FREE (no charge)
  - Storage: Still $0.10/GB/month (charged!)

Elastic IP (unused):
  - Also charges $0.005/hour when not in use!
```

**Cost optimization:**

```bash
# Stopped but still costing for storage
aws ec2 stop-instances --instance-ids i-xxx

# Truly free it up
aws ec2 terminate-instances --instance-ids i-xxx
# But then everything on EC2 is GONE!

# Better: Use snapshots to save state
# Delete EC2 (free)
# When needed, recreate from snapshot
```

---

### Q8: Can you change EC2 instance type after launching? (e.g., from t2.micro to t2.small)

**Answer:**

YES, but requires stopping EC2:

```bash
# Stop EC2 (don't terminate!)
aws ec2 stop-instances --instance-ids i-xxx

# Change instance type
aws ec2 modify-instance-attribute \
  --instance-id i-xxx \
  --instance-type t2.small

# Start again
aws ec2 start-instances --instance-ids i-xxx

# ⚠️ Warning: Might not be allowed for all instance types
# t2 can usually change, some older ones can't
```

**Better: Stop and change instance type in console**

```
EC2 Dashboard:
1. Select instance
2. Right-click → Instance State → Stop
3. Right-click → Instance Settings → Change Instance Type
4. Select new type → Apply
5. Right-click → Instance State → Start
```

---

### Q9: What if security group has inbound rule for port 8000, but no outbound rule? Can API still respond?

**Answer:**

YES! But asymmetrically:

```
Inbound rule: 0.0.0.0:8000 → Allow (Client → EC2)
Outbound rule: None (EC2 → ?)

Client sends request to port 8000:
  ✅ Arrives (inbound rule allows)
  
EC2 processes request:
  ✅ Sends response back
  
Why? AWS stateful firewall:
  - Inbound request → automatically allows response
  - Doesn't require explicit outbound rule
```

**But you might need outbound for:**

```
Outbound scenarios:
1. EC2 calling external API
2. EC2 downloading packages
3. EC2 connecting to RDS
4. EC2 DNS lookups

# If no outbound rule:
# EC2 can't download updates
# EC2 can't call external APIs
# EC2 can respond to requests, but can't initiate outbound

# Solution: Add outbound rule
{
  "IpProtocol": "-1",  # All protocols
  "CidrIp": "0.0.0.0/0",  # All destinations
  "Egress": true  # Outbound
}
```

---

### Q10: If two EC2 instances have public IP, can one reach the other using private IP or must they use public IP?

**Answer:**

BOTH work, private IP is preferred:

```
EC2-1 (private: 10.0.1.10, public: 203.45.1.1)
EC2-2 (private: 10.0.2.20, public: 203.45.2.2)

Same VPC:

# ✅ Using private IP (preferred, no internet)
curl http://10.0.2.20:8000

# ✅ Using public IP (works but slower)
curl http://203.45.2.2:8000

# Private IP advantages:
# - Doesn't use internet bandwidth
# - Faster (stays within AWS network)
# - More secure (no public internet)
# - Cheaper (internal traffic is free)
```

**Different VPC/AWS Account:**

```
# ✅ Using public IP (only option)
curl http://203.45.2.2:8000

# ❌ Using private IP (can't reach across VPC)
curl http://10.0.2.20:8000  # Unreachable!
```

---

### Q11: Can you SSH into EC2 without key pair? What if you lose the key?

**Answer:**

NO! Key pair is required. If lost, it's gone:

```bash
# ✅ With key pair
ssh -i key.pem ubuntu@203.45.1.1

# ❌ Without key (FAILS)
ssh ubuntu@203.45.1.1
# Permission denied (no authentication method)

# If you lose the key.pem file:
# ❌ Can't recover it
# Key only exists locally on your machine
# AWS doesn't store it

# Solution if lost:
# 1. Stop EC2 instance
# 2. Detach root volume
# 3. Attach to another EC2
# 4. Modify authorized_keys
# 5. Reattach volume
# OR
# Terminate and create new EC2 with new key
```

**Prevention:**

```bash
# Backup your key pair!
cp key.pem ~/Documents/backup/
chmod 400 key.pem  # Read-only

# Or use AWS Systems Manager Session Manager
# (no key needed, uses AWS permissions)
```

---

### Q12: Does changing security group rules take effect immediately?

**Answer:**

YES! Rules take effect immediately:

```bash
# Current security group
Inbound: port 8000 blocked

# Add inbound rule
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxx \
  --protocol tcp \
  --port 8000 \
  --cidr 0.0.0.0/0

# Immediately effective!
# Client can now access port 8000
# No EC2 restart needed!
```

**Timeline:**

```
1. Update security group (0 seconds)
2. Rule in effect (immediate)
3. Client can access (immediate)
4. No restart/reload needed
```

---

### Q13: If EC2 has Elastic IP, and you stop/start, does the IP change?

**Answer:**

NO! Elastic IP stays attached:

```bash
# EC2 with Elastic IP (e.g., 203.45.1.1)

# Stop EC2
aws ec2 stop-instances --instance-ids i-xxx
# Elastic IP: Still 203.45.1.1 (attached to EC2)

# Start EC2
aws ec2 start-instances --instance-ids i-xxx
# Elastic IP: Still 203.45.1.1 (same!)

# BUT if you Release Elastic IP:
aws ec2 release-address --allocation-id eipalloc-xxx
# IP goes back to AWS pool
# Later, normal public IP might change on restart
```

**Regular public IP (non-Elastic):**

```bash
# Start/Stop → Public IP might change
# Terminate → Public IP definitely released
# Launch new → New public IP assigned

# Elastic IP (reserved):
# Start/Stop/Restart → Same IP
# Terminate → IP still allocated (you pay!)
# Must release to stop paying
```

---

### Q14: Can you access EC2 database (RDS) from your laptop? Or only from EC2?

**Answer:**

Both possible, but requires configuration:

```
RDS Database:
  - Private IP: 10.0.3.30 (only for EC2 in VPC)
  - Public endpoint: db-instance.abc123.us-east-1.rds.amazonaws.com

From EC2 (no extra config):
  psql -h 10.0.3.30 -U admin  ✅ Works

From laptop (requires public endpoint):
  psql -h db-instance.abc123.us-east-1.rds.amazonaws.com -U admin
  
But security group must allow:
  - Source: Your laptop IP
  - Port: 5432 (PostgreSQL)
```

**Security considerations:**

```bash
# ❌ WRONG (exposes database)
RDS Security Group:
  Inbound: 5432 from 0.0.0.0/0  ← Anyone can access!

# ✅ CORRECT (secure)
RDS Security Group:
  Inbound: 5432 from EC2 security group
  # Only EC2 can access, not laptops
```

---

### Q15: What happens if you terminate an EC2 instance? Is data lost immediately?

**Answer:**

YES! Data is lost immediately if using instance storage:

```
Data types:

1. EBS Volume (Elastic Block Storage)
   - Persistent storage
   - Survives EC2 termination
   - BUT you must explicitly keep it
   
2. Instance Store (Ephemeral)
   - Fast local storage
   - LOST when EC2 terminates
   - Not used by default
   
3. EFS/S3 (External)
   - Separate from EC2
   - Survives termination
```

**Default Dockerfile/docker behavior:**

```bash
docker run -d -p 8000:8000 insurance-api

# Logs are in:
# /var/lib/docker/containers/ (on EBS volume)
# Survives EC2 termination? Only if you:
# 1. Don't delete EBS volume on termination
# 2. Reattach volume to new EC2

# Usually (default):
# EC2 terminates → EBS volume deleted → Data lost!
```

**Prevent data loss:**

```bash
# When creating EC2:
# Storage configuration:
# ☐ Delete on Termination (unchecked = keep volume)

# Or:
# Save to S3 (AWS storage service)
aws s3 cp logs.txt s3://my-bucket/logs.txt
# Data in S3 survives EC2 termination
```

---

### Q16: Can you pause an EC2 instance (not stop/terminate)?

**Answer:**

NO! EC2 only has: Running, Stopped, Terminated

```
EC2 States:
1. Running: Instance is active (charges compute)
2. Stopping: Transition state
3. Stopped: Instance is off (charges storage only)
4. Terminating: Being destroyed
5. Terminated: Deleted (no charges, but data lost)

There's no "Paused" state!

Alternative:
  - Hibernation: Similar effect (saves RAM to disk)
  - But requires special configuration
```

**Lifecycle:**

```
Launch EC2
  ↓
Running (can SSH, use API)
  ↓
Stop (pause work, but keep for later)
  ↓
Start (restart from stopped state)
  ↓
Terminate (delete completely)
```

---

### Q17: If you open port 443 (HTTPS) instead of 80 (HTTP), do you need an SSL certificate?

**Answer:**

YES! HTTPS requires SSL certificate:

```
HTTP (port 80):
  Client ↔ Server
  Data in plain text (insecure)
  No certificate needed

HTTPS (port 443):
  Client ←(encrypted)→ Server
  Data encrypted
  Certificate required
  SSL/TLS handshake
```

**Getting certificate:**

```bash
# Option 1: AWS Certificate Manager (free)
aws acm request-certificate --domain-name example.com

# Option 2: Let's Encrypt (free)
sudo certbot certonly --standalone -d example.com

# Option 3: Self-signed (dev only)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem
```

**Using certificate:**

```bash
# Start FastAPI with HTTPS
uvicorn main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem --port 443

# Client can now access
https://203.45.1.1/  ✅ Encrypted
```

---

### Q18: Can you run multiple applications on same EC2 on different ports?

**Answer:**

YES! Multiple apps on different ports:

```bash
# Terminal 1: FastAPI on port 8000
uvicorn main:app --port 8000

# Terminal 2 (new SSH session): Streamlit on port 8501
streamlit run frontend.py --server.port 8501

# Terminal 3: Another API on port 9000
uvicorn other_app:app --port 9000

# All running simultaneously!
# Access via:
# API: http://203.45.1.1:8000
# Streamlit: http://203.45.1.1:8501
# Other API: http://203.45.1.1:9000
```

**Using Docker (better approach):**

```bash
# docker-compose.yml
version: '3'
services:
  api1:
    ports:
      - "8000:8000"
  api2:
    ports:
      - "8001:8000"
  streamlit:
    ports:
      - "8501:8501"

# All managed together
docker-compose up
```

---

### Q19: Does stopping EC2 lose the Docker image or container?

**Answer:**

NO! Both survive stop/start:

```bash
# EC2 running
docker run -d -p 8000:8000 insurance-api

# Stop EC2
aws ec2 stop-instances --instance-ids i-xxx
# Container: Stopped (but not deleted)
# Image: Stored on disk

# Start EC2
aws ec2 start-instances --instance-ids i-xxx
# Container: Still there, but stopped
# Need to restart it:
docker start <container-id>

# Or recreate:
docker run -d -p 8000:8000 insurance-api
```

**But terminating loses everything:**

```bash
# Terminate EC2
aws ec2 terminate-instances --instance-ids i-xxx

# Result:
# - Container: GONE
# - Image: GONE
# - EBS volume: GONE (if delete on termination is enabled)

# Solution: Save to Docker Hub before terminating
docker push username/insurance-api:latest
# Can recreate from image later
```

---

### Q20: What's the main difference between using EC2 vs Heroku/Railway/Fly.io?

**Answer:**

EC2 = Full control, higher complexity. Heroku = Managed, simpler:

| Aspect | EC2 | Heroku |
|--------|-----|--------|
| **Setup** | Complex (VPC, security, networking) | Simple (just push) |
| **Cost** | $7-10/month (after free tier) | $7-50/month |
| **Scaling** | Manual (add more instances) | Auto-scaling |
| **Maintenance** | You manage OS, updates | Heroku manages |
| **Control** | Full control | Limited customization |
| **Deployment** | git push or manually upload | git push (automatic) |
| **Monitoring** | Manual setup | Built-in |

**EC2 example:**

```bash
# 1. Launch EC2
# 2. SSH and configure OS
# 3. Install dependencies
# 4. Setup systemd/Docker
# 5. Deploy app
# 6. Monitor manually
# 7. Scale by adding instances + load balancer
```

**Heroku example:**

```bash
# 1. Create Procfile
# 2. git push heroku main
# Done! Deployed and running
# Auto-scales
# Built-in monitoring
```

**When to use each:**

```
EC2:
  - Maximum control needed
  - Complex infrastructure
  - Cost-sensitive at scale
  - Running 24/7

Heroku/Railway/Fly.io:
  - Quick deployment
  - Small team
  - Don't want to manage servers
  - Willing to pay for convenience
```

---

## Congratulations! 🎉

You've completed the entire FastAPI journey:

✅ **Chapter 1-6:** Learned FastAPI fundamentals  
✅ **Chapter 7:** Implemented production-grade improvements  
✅ **Chapter 8:** Containerized with Docker  
✅ **Chapter 9:** Deployed to AWS cloud  

**Result:** Professional Machine Learning API accessible to the world!

---

**Next:** Explore advanced topics in Docker_Course and start building your own projects!

**Time: 45-60 minutes | Difficulty: Intermediate | Hands-on: Yes**
