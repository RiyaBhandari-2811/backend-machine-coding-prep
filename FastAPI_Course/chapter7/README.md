# Chapter 7: API Improvements & Refactoring Before Deployment

## 🎯 Overview

Transform a basic FastAPI application into **production-ready code** through systematic improvements and refactoring. This chapter focuses on industry best practices, code organization, and preparing for deployment.

---

## 📊 Chapter 7 Improvements Checklist

```
✅ Improvement #1: Dedicated Project Folder
   └─ Separate folder for API with proper structure

✅ Improvement #2: Field Validation  
   └─ @field_validator for city name normalization

✅ Improvement #3: Home Endpoint
   └─ GET / with API information for humans

✅ Improvement #4: Health Check Endpoint
   └─ GET /health for cloud platforms (AWS, Kubernetes)

✅ Improvement #5: Separation of Concerns
   └─ Separate files: schemas/, config/, models/

✅ Improvement #6: Confidence Scores
   └─ Add predict_proba() for richer output

✅ Improvement #7: Error Handling
   └─ Try-catch blocks for graceful failures

✅ Improvement #8: Response Models
   └─ Pydantic validation for API output
```

---

## 📁 Project Structure

```
insurance_premium_prediction/
├── config/
│   ├── __init__.py
│   └── city_tier.py              # City tier mappings
├── models/
│   ├── __init__.py
│   ├── model.pkl                  # Pre-trained ML model
│   └── predict.py                 # Prediction logic
├── schemas/
│   ├── __init__.py
│   ├── user_input.py              # Input validation
│   └── prediction_response.py      # Output validation
├── main.py                         # FastAPI app + routing
├── requirements.txt                # Dependencies
└── README.md                       # This file
```

---

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
cd chapter7
python -m venv my_env
source my_env/bin/activate  # On Windows: my_env\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run API Server

```bash
uvicorn main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 4. Access API Documentation

Visit: http://localhost:8000/docs

---

## 🔧 Understanding Each Improvement

### Improvement #1: Dedicated Project Folder

**Before:** Mixed with other projects, Jupyter notebooks, patient data, etc.

**After:** Standalone folder ready for containerization

```
insurance_premium_prediction/
├── config/       # Only config files
├── models/       # Only ML model
├── schemas/      # Only data validation
└── main.py       # Only routing
```

**Benefit:** Can be deployed as independent microservice

---

### Improvement #2: Field Validation

**Problem:**
```
User input: "mumbai"  (lowercase)
Expected:   "Mumbai"  (title case)
Result:     Classified as Tier 3 instead of Tier 1
```

**Solution:** Use `@field_validator` in `schemas/user_input.py`

```python
@field_validator('city')
@classmethod
def normalize_city(cls, v):
    return v.strip().title()
```

**Now:**
- `"mumbai"` → `"Mumbai"` ✅
- `"  delhi  "` → `"Delhi"` ✅
- `"BANGALORE"` → `"Bangalore"` ✅

---

### Improvement #3: Home Endpoint

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "Insurance Premium Prediction API",
  "version": "2.0.0",
  "status": "active",
  "endpoints": [
    "GET /",
    "GET /health",
    "POST /predict",
    "GET /docs"
  ]
}
```

**Why?** Users know the API is accessible and operational

---

### Improvement #4: Health Check Endpoint

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "model_version": "1.0.0"
}
```

**Why Cloud Platforms Use This:**
- AWS Elastic Load Balancer checks `/health` every 30 seconds
- Kubernetes uses it for pod readiness probes
- Automated recovery if status != "ok"
- Required for production deployments

---

### Improvement #5: Separation of Concerns

**Principle:** Each file has ONE job

| File | Responsibility |
|------|---|
| `schemas/user_input.py` | Validate input data |
| `schemas/prediction_response.py` | Validate output data |
| `config/city_tier.py` | Configuration (city mappings) |
| `models/predict.py` | ML prediction logic |
| `main.py` | Routing ONLY |

**Before:** 300+ lines in one file  
**After:** 50-100 lines per file

**Benefits:**
- Easy to find code
- Easy to test modules
- Easy to reuse in other projects
- Clear responsibility for each file

---

### Improvement #6: Confidence Scores

**Before:**
```json
{
  "predicted_category": "High"
}
```

**After:**
```json
{
  "predicted_category": "High",
  "confidence": 0.73,
  "class_probabilities": {
    "High": 0.73,
    "Medium": 0.17,
    "Low": 0.10
  }
}
```

**Why?** Users need to know model certainty
- 99% confidence vs 51% confidence = very different!
- Can see alternative classifications
- Better decision-making

---

### Improvement #7: Error Handling

**Before:**
```
Unhandled exception → Server crash
```

**After:**
```python
try:
    result = predict_output(data)
except Exception as e:
    return JSONResponse(
        status_code=500,
        content={"error": str(e)}
    )
```

**Result:** 
- Graceful error response
- Server stays running
- Client gets helpful error message

---

### Improvement #8: Response Models

**Implementation:**
```python
@app.post("/predict", response_model=PredictionResponse)
def predict_premium(user_data: UserInput):
    return predict_output(user_data.model_dump())
```

**Benefits:**

1. **Auto-Documentation** in Swagger

   Before:
   ```
   POST /predict
   Returns: object
   ```

   After:
   ```
   POST /predict
   Returns: PredictionResponse
     - predicted_category: string (example: "High")
     - confidence: float (example: 0.73)
     - class_probabilities: object
   ```

2. **Output Validation** - FastAPI checks response matches schema

3. **Type Safety** - Client knows exact response structure

4. **Examples** - Swagger shows real example responses

---

## 🧪 Testing the API

### Test Home Endpoint

```bash
curl http://localhost:8000/
```

### Test Health Check

```bash
curl http://localhost:8000/health
```

### Test Prediction

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "weight": 79,
    "height": 1.72,
    "income_lpa": 10,
    "smoker": false,
    "city": "mumbai",
    "occupation": "Software Engineer"
  }'
```

**Expected Response:**
```json
{
  "predicted_category": "Low",
  "confidence": 0.39,
  "class_probabilities": {
    "High": 0.36,
    "Medium": 0.25,
    "Low": 0.39
  }
}
```

### Use Swagger UI (Recommended)

1. Visit: http://localhost:8000/docs
2. Click on `/predict` endpoint
3. Click "Try it out"
4. Fill in values
5. Click "Execute"
6. See response

---

## 📊 Before vs After

| Aspect | Before | After |
|--------|--------|-------|
| Files | 1 | 6+ |
| Lines per file | 300+ | 50-100 |
| Home endpoint | ❌ | ✅ |
| Health check | ❌ | ✅ |
| City validation | Basic | ✅ Auto-normalized |
| Confidence scores | ❌ | ✅ |
| Error handling | ❌ | ✅ |
| Response validation | ❌ | ✅ |
| Docker-ready | ❌ | ✅ |
| Production-ready | ❌ | ✅ |

---

## 🎓 Key Concepts

### Separation of Concerns
Each module handles ONE responsibility:
- Schemas: Data validation
- Config: Settings
- Models: ML logic
- Main: Routing

### @field_validator
Preprocess and validate input fields:
```python
@field_validator('city')
def normalize_city(cls, v):
    return v.strip().title()
```

### response_model
Validate API output:
```python
@app.post("/predict", response_model=PredictionResponse)
```

### Health Check
Required by cloud platforms. Return status and version.

### Confidence Scores
Use `predict_proba()` for model probabilities.

---

## 🚀 Next Steps

**Chapter 8:** Dockerize this application
- Create Dockerfile
- Build Docker image
- Run container locally

**Chapter 9:** Deploy to AWS
- Push image to ECR
- Run on ECS
- Set up load balancer

---

## 📚 File Descriptions

| File | Lines | Purpose |
|------|-------|---------|
| main.py | ~250 | FastAPI app with routing only |
| schemas/user_input.py | ~95 | Input validation + field normalization |
| schemas/prediction_response.py | ~50 | Output validation |
| config/city_tier.py | ~35 | City tier mappings |
| models/predict.py | ~150 | ML model loading and prediction |
| requirements.txt | 5 | Python dependencies |
| chapter7.md | 450+ | Detailed guide |

**Total: 1,030+ lines of production-ready code**

---

## ✨ Highlights

✅ **Clean Code** - Each file does ONE thing  
✅ **Well Documented** - Comments explain why, not just what  
✅ **Production-Ready** - Error handling, validation, health checks  
✅ **Easy to Test** - Modular structure enables unit tests  
✅ **Easy to Extend** - Add new endpoints without touching existing code  
✅ **Docker-Ready** - Proper structure for containerization  
✅ **Cloud-Ready** - Health check endpoint for auto-scaling  

---

## 🎯 Interview Questions

**Q: Why separate code into different files?**
A: Separation of concerns. Each file has one job. Easier to test, reuse, and maintain.

**Q: What's a health check endpoint?**
A: Machine-readable endpoint that tells cloud platforms if API is healthy. AWS/Kubernetes use it.

**Q: Why validate city name?**
A: Ensure consistency. "mumbai" and "Mumbai" should be treated the same.

**Q: What's a response model?**
A: Pydantic model that validates API output. Ensures consistent response format.

**Q: Why add confidence scores?**
A: Users need to know how certain the model is. Different decision-making if 99% vs 51%.

**Q: How handle errors gracefully?**
A: Use try-catch blocks. Return meaningful error (status 500) instead of crashing.

---

## 📖 Files Structure Explained

```
schemas/           # Data Validation Layer
├── user_input.py          # Validates user input + normalizes
└── prediction_response.py  # Validates API output

config/            # Configuration Layer
└── city_tier.py           # Settings (city mappings)

models/            # ML Logic Layer
├── model.pkl              # Pre-trained model
└── predict.py             # Prediction + feature computation

main.py            # Routing Layer
                   # Orchestrates all layers
```

---

**Ready for Docker & Cloud Deployment! 🚀**
