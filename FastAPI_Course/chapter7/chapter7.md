# Chapter 7: API Improvements & Refactoring Before Deployment

## Overview

Transform your basic FastAPI application into **production-ready code** through systematic improvements and refactoring. This chapter focuses on best practices for code organization, validation, and output enrichment.

---

## 🎯 8 Major Improvements

### 1. **Dedicated Project Folder** ✅
- Separate folder per API project
- Clean isolated development environment
- Ready for containerization

### 2. **Field Validation** ✅
- Auto-normalize city names to title case
- Consistent data handling
- Use `@field_validator` for preprocessing

### 3. **Home Endpoint** ✅
- Human-readable API info
- First impression for clients
- Shows API is alive and healthy

### 4. **Health Check Endpoint** ✅
- Machine-readable status endpoint
- Required by cloud platforms (AWS, Kubernetes)
- Reports model version and status

### 5. **Separation of Concerns** ✅
- Schemas folder: Pydantic models
- Config folder: Configuration data
- Models folder: ML prediction logic
- Main.py: Only routing logic

### 6. **Confidence Scores** ✅
- Add `predict_proba()` output
- Show probability for all classes
- Richer information to clients

### 7. **Error Handling** ✅
- Try-catch blocks for external calls
- Graceful error responses
- Prevent server crashes

### 8. **Response Models** ✅
- Validate API output with Pydantic
- Self-documenting API with examples
- Filter unnecessary data

---

## 📁 Project Structure

```
insurance_premium_prediction/
├── config/
│   └── city_tier.py          # City tier mappings
├── models/
│   ├── model.pkl              # Pre-trained ML model
│   └── predict.py             # Prediction logic
├── schemas/
│   ├── user_input.py          # Input validation
│   └── prediction_response.py  # Output validation
├── main.py                     # FastAPI app + routing
├── requirements.txt            # Dependencies
└── README.md                   # Documentation
```

---

## 🔧 Improvement #1: Project Structure

### Before (Monolithic)
```
project/
├── app.py                      (everything mixed)
├── model.pkl
├── frontend.py
├── jupyter_notebooks/
├── patients.json
└── other_files.json
```

**Problems:**
- Hard to find code
- Dependencies unclear
- Not ready for Docker
- Mixing concerns

### After (Organized)
```
insurance_premium_prediction/
├── config/
├── models/
├── schemas/
└── main.py (clean routing only)
```

**Benefits:**
- Clear separation
- Easy to navigate
- Docker-ready
- Scalable structure

---

## 🔧 Improvement #2: Field Validation

### Problem: City Name Inconsistency

**User Input:** `"mumbai"` (lowercase)  
**Expected:** `"Mumbai"` (title case)  
**Issue:** City tier matching fails → Classified as Tier 3

### Solution: @field_validator

```python
from pydantic import field_validator

class UserInput(BaseModel):
    city: str
    
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v):
        """Normalize city to title case."""
        return v.strip().title()
```

**Result:**
- `"mumbai"` → `"Mumbai"` ✅
- `"  delhi  "` → `"Delhi"` ✅
- Works transparently for all inputs

---

## 🔧 Improvement #3: Home Endpoint

### Why?
- Users should know API is accessible
- Shows this is an API (not a website)
- Common REST API convention
- Human-friendly information

### Implementation

```python
@app.get("/")
def home():
    """Root endpoint with API information."""
    return {
        "message": "Insurance Premium Prediction API",
        "version": "2.0.0",
        "status": "active",
        "endpoints": ["/", "/health", "/predict", "/docs"]
    }
```

### Test
```bash
curl http://localhost:8000/
```

---

## 🔧 Improvement #4: Health Check Endpoint

### Why?
- Cloud platforms require it (AWS, Kubernetes)
- Automated monitoring and recovery
- Machine-readable format
- Reports system status

### Implementation

```python
@app.get("/health")
def health_check():
    """Health check endpoint for cloud platforms."""
    return {
        "status": "ok",
        "model_loaded": True,
        "model_version": "1.0.0"
    }
```

### Usage
- **AWS Elastic Load Balancer:** Hits `/health` every 30 seconds
- **Kubernetes:** Uses health check for pod readiness
- **Monitoring:** Automated alerts if status != "ok"

### Test
```bash
curl http://localhost:8000/health
# Expected: {"status":"ok","model_loaded":true,"model_version":"1.0.0"}
```

---

## 🔧 Improvement #5: Separation of Concerns

### Principle
> **Each file should have one responsibility**

### Anti-pattern (Don't Do This)
```python
# BAD: Everything in app.py
from pydantic import BaseModel
from fastapi import FastAPI
import pickle
import pandas as pd

class UserInput(BaseModel):
    ...

model = pickle.load(...)

def predict():
    ...

app = FastAPI()
...
```

### Pattern (Do This) ✅

**schemas/user_input.py** - Input validation
```python
from pydantic import BaseModel, field_validator

class UserInput(BaseModel):
    age: int
    weight: float
    ...
```

**models/predict.py** - ML logic
```python
import pickle

def predict_output(user_input):
    model = load_model()
    prediction = model.predict(...)
    return prediction
```

**main.py** - Just routing
```python
from schemas.user_input import UserInput
from models.predict import predict_output

@app.post("/predict")
def predict(data: UserInput):
    result = predict_output(data.model_dump())
    return result
```

### Benefits
| Benefit | How It Helps |
|---------|---|
| **Readability** | Find code quickly |
| **Testing** | Test modules independently |
| **Reusability** | Use schemas/models in other projects |
| **Maintenance** | Update models without touching routing |
| **Scaling** | Add new endpoints easily |

---

## 🔧 Improvement #6: Confidence Scores

### Before
```json
{
  "predicted_category": "High"
}
```

**Problem:** No confidence! User doesn't know if model is 99% or 51% sure.

### After
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

**Benefit:** User sees full picture!
- If confidence is low (0.34), user can be cautious
- Can see alternative classifications
- Better decision-making

### Implementation

```python
def predict_output(user_input: dict):
    model = load_model()
    input_df = pd.DataFrame([user_input])
    
    # Get prediction
    prediction = model.predict(input_df)[0]
    
    # Get probabilities
    probabilities = model.predict_proba(input_df)[0]
    class_names = model.classes_
    
    # Build response
    prob_dict = {name: float(prob) 
                 for name, prob in zip(class_names, probabilities)}
    
    return {
        "predicted_category": prediction,
        "confidence": float(prob_dict[prediction]),
        "class_probabilities": prob_dict
    }
```

---

## 🔧 Improvement #7: Error Handling

### Problem
External dependencies can fail (ML model, file loading). Unhandled exceptions crash the server.

### Solution: Try-Catch Blocks

```python
from fastapi.responses import JSONResponse

@app.post("/predict")
def predict(data: UserInput):
    try:
        result = predict_output(data.model_dump())
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
```

**What happens:**
| Case | Before | After |
|------|--------|-------|
| Prediction succeeds | ✅ 200 OK | ✅ 200 OK |
| Model crashes | ❌ 500 (generic) | ✅ 500 + error message |
| File not found | ❌ 500 (generic) | ✅ 500 + specific error |

---

## 🔧 Improvement #8: Response Models

### Problem
Client doesn't know expected output format or what fields are optional.

### Solution: Pydantic Response Model

**schemas/prediction_response.py**
```python
from pydantic import BaseModel, Field

class PredictionResponse(BaseModel):
    predicted_category: str = Field(
        ..., 
        description="Predicted premium category",
        examples=["High", "Medium", "Low"]
    )
    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confidence score (0-1)",
        examples=[0.73]
    )
    class_probabilities: dict = Field(
        ...,
        description="Probability for each class",
        examples=[{"High": 0.73, "Medium": 0.17, "Low": 0.10}]
    )
```

**main.py**
```python
@app.post("/predict", response_model=PredictionResponse)
def predict(data: UserInput):
    return predict_output(data.model_dump())
```

### Benefits

1. **Auto Documentation** - Swagger shows expected output format
2. **Validation** - Output checked before sending to client
3. **Type Safety** - Client knows exact response structure
4. **Examples** - Swagger shows real examples

### Swagger UI Impact

**Before:**
```
POST /predict
Returns: object
```

**After:**
```
POST /predict
Returns: PredictionResponse
  - predicted_category: string (example: "High")
  - confidence: number (example: 0.73)
  - class_probabilities: object (example: {...})
```

---

## 📊 Before vs After Comparison

| Aspect | Before | After |
|--------|--------|-------|
| **Files** | 1 (app.py) | 6+ (separated) |
| **Lines per file** | 300+ | 50-100 (focused) |
| **Home endpoint** | ❌ None | ✅ GET / |
| **Health check** | ❌ None | ✅ GET /health |
| **Output format** | Basic string | Rich with confidence |
| **Response validation** | ❌ None | ✅ Pydantic model |
| **Error handling** | ❌ Crashes | ✅ Graceful errors |
| **Field validation** | Basic | ✅ Auto-normalize |
| **Docker-ready** | ❌ No | ✅ Yes |
| **Production-ready** | ❌ No | ✅ Yes |

---

## 🎓 Interview Questions

**Q: Why separate code into different files?**
A: Separation of concerns. Each file has one job. Easier to test, reuse, and maintain.

**Q: What's a health check endpoint?**
A: Machine-readable endpoint that tells cloud platforms if API is healthy. Required for auto-recovery.

**Q: Why validate city name?**
A: Ensure consistent data. `"mumbai"` and `"Mumbai"` should be treated the same.

**Q: What's a response model?**
A: Pydantic model that validates API output. Ensures consistent response format.

**Q: Why add confidence scores?**
A: Users need to know how certain the model is. 99% confidence is different from 51%.

**Q: How to handle errors gracefully?**
A: Use try-catch blocks. Return meaningful error messages (status 500) instead of crashing.

**Q: What folder structure is best?**
A: `schemas/` for models, `config/` for settings, `models/` for ML logic, `main.py` for routing.

**Q: Why not keep everything in one file?**
A: Hard to read, test, and scale. Harder to work in teams. Not Docker-friendly.

**Q: What's `@field_validator`?**
A: Pydantic decorator for custom validation/preprocessing before model creation.

**Q: How does response_model improve Swagger?**
A: Shows exact response format with examples. Clients know what to expect.

---

## 🚀 Next Steps

After these improvements:
1. ✅ Code is clean and organized
2. ✅ Production-ready structure
3. ✅ Ready for Docker containerization (Chapter 8)
4. ✅ Ready for cloud deployment (Chapter 9)

---

## 📚 Files in This Chapter

| File | Lines | Purpose |
|------|-------|---------|
| chapter7.md | ~450 | This guide |
| main.py | ~250 | Refactored API |
| schemas/user_input.py | ~150 | Input validation |
| schemas/prediction_response.py | ~50 | Output validation |
| config/city_tier.py | ~20 | City mappings |
| models/predict.py | ~100 | ML logic |
| requirements.txt | ~10 | Dependencies |

**Total: 1,030 lines of production-ready code**

---

## 🎯 Key Takeaways

✅ **Separate concerns** - Different files for different purposes  
✅ **Validate input** - Use @field_validator for preprocessing  
✅ **Validate output** - Use response_model for consistency  
✅ **Add health checks** - Required for cloud platforms  
✅ **Add confidence** - Enrich predictions with probabilities  
✅ **Handle errors** - Try-catch to prevent crashes  
✅ **Document well** - Add examples and descriptions  
✅ **Clean structure** - Docker and scalability ready

---

**Ready for deployment! 🚀**
