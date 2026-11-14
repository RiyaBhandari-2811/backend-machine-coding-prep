# AWS EC2 Deployment Checklist

Complete this checklist as you deploy your FastAPI application to AWS.

## 🔷 Phase 1: AWS Account & EC2 Setup

### Account Setup
- [ ] Created AWS account at https://aws.amazon.com
- [ ] Verified email address
- [ ] Added payment method (for free tier verification)
- [ ] Signed into AWS Management Console
- [ ] Confirmed free tier eligibility

### EC2 Instance Configuration
- [ ] Navigated to EC2 service
- [ ] Clicked "Instances" → "Launch Instance"
- [ ] Set instance name to `MyFastAPIServer`
- [ ] Selected Ubuntu Server 22.04 LTS AMI
- [ ] Chose t2.micro instance type (**FREE**)
- [ ] Created/selected SSH key pair
  - [ ] Downloaded `.pem` file (if new)
  - [ ] Stored in secure location
  - [ ] Set permissions: `chmod 400 key.pem`
- [ ] Configured network settings
  - [ ] ✅ Allow SSH traffic (Port 22)
  - [ ] ✅ Create security group
- [ ] Set storage to 8GB
- [ ] Launched instance
- [ ] Instance State shows "running"
- [ ] Noted Public IPv4 address

**Public IP Address:** `_____________________`

---

## 🔷 Phase 2: Connect & Install Docker

### Connect to EC2
- [ ] Used browser-based terminal (Connect button)
  OR
- [ ] Connected via SSH:
  ```bash
  ssh -i api-aws-key.pem ubuntu@YOUR_PUBLIC_IP
  ```

### System Updates
- [ ] Ran: `sudo apt update`
- [ ] Ran: `sudo apt upgrade -y`
- [ ] No errors in output

### Install Docker
- [ ] Ran: `sudo apt install -y docker.io`
- [ ] Ran: `sudo systemctl start docker`
- [ ] Ran: `sudo systemctl enable docker`
- [ ] Ran: `sudo usermod -aG docker ubuntu`
- [ ] Verified with: `docker --version`
- [ ] Output shows Docker version

### Grant Permissions
- [ ] Exited connection: `exit`
- [ ] Reconnected to EC2 (terminal or SSH)
- [ ] Tested: `docker ps` (no sudo needed)
- [ ] Output shows no errors

---

## 🔷 Phase 3: Pull & Run Docker Image

### Pull from Docker Hub
- [ ] Ran: `docker pull YOUR_USERNAME/insurance-api:1.0`
- [ ] Image downloaded successfully
- [ ] No authentication errors
- [ ] Verified with: `docker images`
- [ ] Image appears in list

### Run Container
- [ ] Ran: `docker run -d -p 8000:8000 YOUR_USERNAME/insurance-api:1.0`
- [ ] Got a container ID in output
- [ ] Ran: `docker ps`
- [ ] Container shows "Up" status
- [ ] Port shows `0.0.0.0:8000->8000/tcp`

**Container ID:** `_____________________`

### Verify Container Health
- [ ] Ran: `docker logs container_id`
- [ ] Logs show Uvicorn server starting
- [ ] No error messages
- [ ] Logs show "Application startup complete"

---

## 🔷 Phase 4: Configure Security Group

### Access Security Settings
- [ ] Went to EC2 Instances list
- [ ] Selected the running instance
- [ ] Clicked "Security" tab
- [ ] Noted security group name
- [ ] Clicked on security group link

### Edit Inbound Rules
- [ ] Clicked "Edit inbound rules" button
- [ ] Noted existing SSH rule (Port 22)

### Add Custom Rule for Port 8000
- [ ] Clicked "Add rule"
- [ ] Set Type: **Custom TCP**
- [ ] Set Port Range: **8000**
- [ ] Set Source: **0.0.0.0/0** (anywhere)
- [ ] Clicked "Save rules"
- [ ] Confirmation message appeared
- [ ] New rule visible in list

### Current Security Rules
```
Protocol    Port    Source      Purpose
TCP         22      Your IP     SSH management
TCP         8000    0.0.0.0/0   API access
```

---

## 🔷 Phase 5: Test API Access

### Get Public IP
- [ ] Went back to Instances
- [ ] Selected instance
- [ ] Copied "Public IPv4" address
- [ ] Format: `XXX.XXX.XXX.XXX`

**Your Public IP:** `_____________________`

### Test Endpoints

#### Home Endpoint
- [ ] Opened browser
- [ ] Navigated to: `http://YOUR_IP:8000`
- [ ] Saw JSON response
- [ ] Response includes message, version, endpoints

#### Health Check
- [ ] Opened: `http://YOUR_IP:8000/health`
- [ ] Saw health status
- [ ] Response shows: `{"status": "healthy"}`

#### API Documentation
- [ ] Opened: `http://YOUR_IP:8000/docs`
- [ ] Swagger UI loaded successfully
- [ ] All endpoints visible
- [ ] Can interact with API

### Test Prediction Endpoint
- [ ] In Swagger UI, scrolled to `/predict`
- [ ] Clicked "Try it out"
- [ ] Filled in sample data:
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
- [ ] Clicked "Execute"
- [ ] Got prediction response
- [ ] Response includes: predicted_category, confidence, class_probabilities

**Expected Response:**
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

---

## 🔷 Phase 6: Setup Streamlit Frontend

### Create Streamlit App
- [ ] Created file: `streamlit_app.py`
- [ ] Copied code from chapter9 materials
- [ ] Located section: `API_BASE_URL = "http://YOUR_AWS_IP:8000"`

### Update API URL
- [ ] Replaced `YOUR_AWS_IP` with actual IP address
- [ ] Example: `http://54.123.45.67:8000`
- [ ] Verified no typos
- [ ] Saved file

### Install Dependencies
- [ ] Ran: `pip install streamlit requests`
- [ ] Both packages installed successfully

### Run Streamlit
- [ ] Ran: `streamlit run streamlit_app.py`
- [ ] Streamlit started
- [ ] Browser opened to: `http://localhost:8501`
- [ ] App loaded successfully

### Test Streamlit App
- [ ] Filled in form fields:
  - [ ] Age: 31
  - [ ] Weight: 91
  - [ ] Height: 1.72
  - [ ] Income: 10
  - [ ] Smoker: Checked
  - [ ] City: gurgaon
- [ ] Clicked "Predict Insurance Premium"
- [ ] App made request to AWS API
- [ ] Got prediction result
- [ ] Displayed in app
- [ ] No error messages

### Test Health Check (in Streamlit)
- [ ] Clicked "Check API Status" button
- [ ] Saw health status
- [ ] Status shows "healthy"

---

## 🔷 Phase 7: Verify End-to-End Flow

### Complete Workflow
- [ ] ✅ Docker image on Docker Hub
- [ ] ✅ AWS EC2 instance running
- [ ] ✅ Docker installed on EC2
- [ ] ✅ Image pulled from Docker Hub
- [ ] ✅ Container running on EC2
- [ ] ✅ Security group configured
- [ ] ✅ API accessible via public IP
- [ ] ✅ Swagger UI working
- [ ] ✅ Prediction endpoint working
- [ ] ✅ Streamlit frontend working
- [ ] ✅ Streamlit connects to AWS API
- [ ] ✅ Full prediction flow working

### Test Multiple Scenarios

**Test Case 1: Low Risk Profile**
- [ ] Age: 25, Weight: 60, Height: 1.75
- [ ] Income: 5, Smoker: No, City: bangalore
- [ ] Expected: Low or Medium category

**Test Case 2: High Risk Profile**
- [ ] Age: 55, Weight: 95, Height: 1.70
- [ ] Income: 20, Smoker: Yes, City: delhi
- [ ] Expected: High category

**Test Case 3: Edge Cases**
- [ ] Age: 18 (minimum)
- [ ] Age: 100 (maximum)
- [ ] Income: 1 (minimum)
- [ ] Income: 200 (maximum)

---

## 🔷 Phase 8: Monitoring & Maintenance

### Monitor Container
- [ ] SSH into EC2
- [ ] Ran: `docker ps` → Container running
- [ ] Ran: `docker logs container_id` → No errors
- [ ] Ran: `docker stats` → Resources OK
  - [ ] CPU usage < 30%
  - [ ] Memory usage < 256 MB

### Monitor EC2
- [ ] AWS Console → EC2 Dashboard
- [ ] Instance state: Running
- [ ] CPU utilization: Normal
- [ ] No alarm notifications
- [ ] Security group rules: Correct

### Test API Availability
- [ ] Checked API from browser: ✅
- [ ] Tested from Streamlit: ✅
- [ ] Checked health endpoint: ✅
- [ ] Checked documentation: ✅

### Verify Billing
- [ ] Checked AWS Billing console
- [ ] t2.micro usage: Within free tier
- [ ] Data transfer: Within 15GB limit
- [ ] Set billing alerts (recommended)

---

## 🔷 Phase 9: Documentation & Handoff

### Document Your Setup
- [ ] Public API IP: `_____________________`
- [ ] Streamlit App: Running on localhost:8501
- [ ] API Documentation: `http://YOUR_IP:8000/docs`
- [ ] Container ID: `_____________________`
- [ ] Key pair location: `_____________________`

### Create README
- [ ] Documented how to access API
- [ ] Listed all endpoints
- [ ] Provided test examples
- [ ] Added troubleshooting section

### Backup Important Info
- [ ] Saved AWS IP address
- [ ] Saved Security Group ID
- [ ] Saved Instance ID
- [ ] Backed up key pair file
- [ ] Documented configuration

---

## 🟢 Deployment Complete!

Once all items are checked, your deployment is complete! ✅

### What You've Accomplished

✅ **Deployed API to AWS** - Now publicly accessible  
✅ **Containerized application** - Using Docker  
✅ **Configured security** - With security groups  
✅ **Built frontend** - Streamlit dashboard  
✅ **Integrated systems** - Frontend connects to backend  
✅ **Tested thoroughly** - All endpoints verified  
✅ **Documented setup** - For future reference  

### Your API is Now:

- 🌍 Globally accessible on internet
- 📍 Running on AWS infrastructure
- 🔒 Secured with security groups
- 🖥️ Accessed via public IP
- 🚀 Ready for production use

### Next Steps

Consider:
- [ ] Setup HTTPS/SSL certificate
- [ ] Add authentication layer
- [ ] Setup auto-scaling
- [ ] Add database persistence
- [ ] Implement CI/CD pipeline
- [ ] Monitor with CloudWatch
- [ ] Implement load balancing

---

## ⚠️ Troubleshooting Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Can't access API | Check security group allows port 8000 |
| Container exited | Check: `docker logs container_id` |
| Can't SSH to EC2 | Use browser terminal instead |
| Timeout errors | Check EC2 CPU/memory usage |
| API returns error | Restart container: `docker restart ID` |
| Streamlit can't connect | Update API_BASE_URL with correct IP |

---

**Deployment Date:** `_____________________`  
**Last Verified:** `_____________________`  
**Status:** ✅ LIVE
