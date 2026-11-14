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

**Q1: Why separate code into different files?**
A: Separation of concerns. Each file has one job. Easier to test, reuse, and maintain.

**Q2: What's a health check endpoint?**
A: Machine-readable endpoint that tells cloud platforms if API is healthy. Required for auto-recovery.

**Q3: Why validate city name?**
A: Ensure consistent data. `"mumbai"` and `"Mumbai"` should be treated the same.

**Q4: What's a response model?**
A: Pydantic model that validates API output. Ensures consistent response format.

**Q5: Why add confidence scores?**
A: Users need to know how certain the model is. 99% confidence is different from 51%.

**Q6: How to handle errors gracefully?**
A: Use try-catch blocks. Return meaningful error messages (status 500) instead of crashing.

**Q7: What folder structure is best?**
A: `schemas/` for models, `config/` for settings, `models/` for ML logic, `main.py` for routing.

**Q8: Why not keep everything in one file?**
A: Hard to read, test, and scale. Harder to work in teams. Not Docker-friendly.

**Q9: What's `@field_validator`?**
A: Pydantic decorator for custom validation/preprocessing before model creation.

**Q10: How does response_model improve Swagger?**
A: Shows exact response format with examples. Clients know what to expect.

---

## 🤔 Confusing Questions (Follow-Up Interview Questions)

### Q11: What's the difference between input validation (request body) and output validation (response)?

**Answer:**

They happen at different stages:

```python
# INPUT validation (before business logic)
@app.post("/predict")
async def predict(data: UserInput):  # ← Pydantic validates here
    # If data is invalid, FastAPI returns 422 immediately
    # Business logic never runs
    
    # If we reach here, data is 100% valid
    prediction = model.predict(...)
    return PredictionResponse(...)  # ← Output validation happens here

# OUTPUT validation (after business logic)
# If response_model is defined, FastAPI validates response
# Before sending to client
```

**Example flow:**

```
Client sends request
  ↓
UserInput validation (Pydantic) ← Q11 focused on this
  ❌ If invalid → 422 error returned to client
  ✅ If valid → Proceed to business logic
  ↓
Business logic runs (model prediction)
  ↓
PredictionResponse validation (Pydantic) ← Also important
  ❌ If response doesn't match model → 500 error (we messed up!)
  ✅ If valid → Send to client
```

---

### Q12: Can you have a field_validator that rejects VALID input based on business logic?

**Answer:**

YES! Validators can check business rules, not just data types:

```python
from pydantic import BaseModel, field_validator

class UserInput(BaseModel):
    age: int
    income: float
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        if v < 0:  # ← Type validation
            raise ValueError("Age must be positive")
        if v > 150:  # ← Business logic validation
            raise ValueError("Age unrealistic")
        if v < 18:  # ← Business rule validation
            raise ValueError("Must be 18+")
        return v
    
    @field_validator('income')
    @classmethod
    def validate_income(cls, v):
        if v < 0:  # ← Invalid value
            raise ValueError("Income must be positive")
        if v > 10_000_000:  # ← Business rule (too high)
            raise ValueError("Income unrealistic")
        return v

# Usage
try:
    user = UserInput(age=25, income=100_000)  # ✅ Valid
except ValueError as e:
    print(f"Error: {e}")

try:
    user = UserInput(age=15, income=50_000)  # ❌ Rejected (business rule)
except ValueError as e:
    print(f"Error: {e}")  # "Must be 18+"
```

---

### Q13: If a field_validator modifies a field, does the response include the modified value?

**Answer:**

YES! The modified value is used:

```python
from pydantic import BaseModel, field_validator

class UserInput(BaseModel):
    city: str
    
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v):
        return v.title()  # ← Modifies value

# Client sends
# {"city": "mumbai"}

user = UserInput(city="mumbai")
print(user.city)  # "Mumbai" (modified by validator!)

# Response would include modified value
print(user.model_dump())
# {"city": "Mumbai"}
```

**This is useful for:**
```python
# Trimming whitespace
@field_validator('name')
def trim_name(cls, v):
    return v.strip()

# Lowercase email
@field_validator('email')
def normalize_email(cls, v):
    return v.lower()

# Remove non-digits from phone
@field_validator('phone')
def clean_phone(cls, v):
    return ''.join(c for c in v if c.isdigit())
```

---

### Q14: Can you use response_model to EXCLUDE certain fields from response?

**Answer:**

YES! You can create a different model for responses:

```python
from pydantic import BaseModel

# Full internal model (includes sensitive data)
class UserInternal(BaseModel):
    name: str
    age: int
    income: float  # ← Sensitive!
    password_hash: str  # ← Sensitive!

# Public response model (excludes sensitive)
class UserPublic(BaseModel):
    name: str
    age: int

@app.get("/users/{user_id}", response_model=UserPublic)
async def get_user(user_id: int):
    # Fetch full user
    user = UserInternal(
        name="John",
        age=30,
        income=100_000,
        password_hash="xyz123"
    )
    
    # Return user (response_model filters it)
    return user
    # Response sent: {"name": "John", "age": 30}
    # income and password_hash are EXCLUDED!
```

**More filtering options:**

```python
# Exclude by field names
response_model_exclude={"password_hash", "income"}

# Include only certain fields
response_model_include={"name", "age"}

# Exclude nested fields
response_model_exclude={"user": {"password_hash"}}
```

---

### Q15: Can a health check endpoint return 500 if model is not loaded? Or should it always return 200?

**Answer:**

A health check should return 503 (Service Unavailable) if critical components fail:

```python
@app.get("/health")
async def health_check():
    status = {
        "status": "ok",
        "model_loaded": model is not None,
        "database_connected": True
    }
    
    # ❌ WRONG - Always return 200
    # return status

    # ✅ CORRECT - Return 503 if unhealthy
    if model is None:
        # Load model failed!
        raise HTTPException(
            status_code=503,
            detail="Model not loaded"
        )
    
    return status  # Returns 200 OK if healthy
```

**Status codes for health checks:**

| Status | Meaning | Action |
|--------|---------|--------|
| 200 OK | Healthy | Route traffic |
| 503 Service Unavailable | Unhealthy | Don't route traffic |
| 500 Internal Server Error | Crashed | Alert ops team |

**Cloud platforms (Kubernetes, AWS) use health check status:**

```
Continuously: GET /health
If 200: Traffic routed ✅
If 503: Pod removed from load balancer 🔴
If timeout (>5s): Pod marked unhealthy
```

---

### Q16: What if a field_validator raises an exception? Can you catch it in the endpoint?

**Answer:**

NO! Validator exceptions are caught by FastAPI:

```python
class UserInput(BaseModel):
    age: int
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        raise ValueError("Age invalid!")

@app.post("/predict")
async def predict(data: UserInput):
    # ❌ You NEVER reach here if validation fails!
    print(f"Age: {data.age}")

# Client POST: {"age": -5}
# FastAPI catches validator exception
# Returns: 422 Unprocessable Entity
# Endpoint never executed!
```

**If you want custom error handling:**

```python
# Option 1: Catch before Pydantic (manual parsing)
@app.post("/predict")
async def predict(data: dict):
    try:
        user = UserInput(**data)
    except ValidationError as e:
        # Handle custom error
        return {"error": str(e), "status": "invalid"}

# Option 2: Use exception handler
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # Custom handling of all 422 errors
    return {"error": "Custom validation error"}
```

---

### Q17: Can you have validators for nested models? Like validate a field inside a nested Pydantic model?

**Answer:**

YES! Validators work for nested models too:

```python
class Address(BaseModel):
    city: str
    
    @field_validator('city')
    @classmethod
    def validate_city(cls, v):
        if v not in ["Mumbai", "Delhi", "Bangalore"]:
            raise ValueError(f"Unsupported city: {v}")
        return v

class UserInput(BaseModel):
    name: str
    address: Address  # ← Nested model

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if len(v) < 2:
            raise ValueError("Name too short")
        return v

# Usage
try:
    user = UserInput(
        name="John",
        address={"city": "Mumbai"}
    )
    print(f"Valid: {user}")
except ValidationError as e:
    print(f"Error: {e}")

# Try invalid city
try:
    user = UserInput(
        name="John",
        address={"city": "Paris"}  # ← Not in allowed list
    )
except ValidationError as e:
    print("Error: Unsupported city: Paris")  # ← Nested validation
```

---

### Q18: Can you use `response_model` to add fields that don't exist in the actual object?

**Answer:**

NO! response_model can only work with fields that exist:

```python
# ❌ WRONG - response_model adds new field
class UserPublic(BaseModel):
    name: str
    age: int
    created_at: datetime  # ← Doesn't exist in UserInternal!

@app.get("/user")
async def get_user():
    user = {"name": "John", "age": 30}
    return user  # Returns dict
    # response_model expects created_at
    # But data doesn't have it
    # Error! Validation fails!


# ✅ CORRECT - Provide all fields
@app.get("/user")
async def get_user():
    from datetime import datetime
    user = {
        "name": "John",
        "age": 30,
        "created_at": datetime.now()  # ← Include it
    }
    return user  # response_model validation succeeds
```

**If you need computed fields in response:**

```python
from pydantic import BaseModel, computed_field

class UserPublic(BaseModel):
    name: str
    age: int
    
    @computed_field
    @property
    def display_name(self) -> str:
        return f"{self.name} (age {self.age})"

@app.get("/user", response_model=UserPublic)
async def get_user():
    user = {"name": "John", "age": 30}
    return UserPublic(**user)
    # response_model includes computed field!
    # Returns: {"name": "John", "age": 30, "display_name": "John (age 30)"}
```

---

### Q19: What's the performance impact of validation? Does every request get validated?

**Answer:**

YES! Every request is validated. Performance impact is NEGLIGIBLE:

```python
# Validation happens for EVERY request:
@app.post("/predict")
async def predict(data: UserInput):
    # 1. Receive request
    # 2. Parse JSON
    # 3. ← VALIDATE with Pydantic (microseconds!)
    # 4. Execute business logic
    # 5. Validate response (microseconds!)
    # 6. Return response

# Performance: 
# - Validation: ~0.1-1ms (negligible)
# - Business logic: ~100-1000ms (dominant)

# Example timings:
# Total request: 500ms
#   - JSON parsing: 1ms
#   - Input validation: 0.5ms
#   - Model prediction: 497ms
#   - Output validation: 0.5ms
#   - Response: 1ms

# Validation is NOT the bottleneck!
```

**When validation CAN be slow:**

```python
# ❌ SLOW - Validation with DB query
@field_validator('email')
@classmethod
def check_email_unique(cls, v):
    # DB query for every request!
    db.query(f"SELECT * FROM users WHERE email='{v}'")
    return v

# ✅ FAST - No DB in validator
@field_validator('email')
@classmethod
def validate_email_format(cls, v):
    # Just format check
    if '@' not in v:
        raise ValueError("Invalid email")
    return v

# DB checks → Put in endpoint logic, not validator
```

---

### Q20: Can you mix manual validation and Pydantic validation in the same endpoint?

**Answer:**

YES, but redundant. Use Pydantic for everything if possible:

```python
# ❌ BAD - Mixing manual + Pydantic
@app.post("/predict")
async def predict(data: UserInput):
    # Pydantic already validated data.age (0-150)
    
    # Don't repeat validation!
    if data.age < 0:  # ← Redundant
        raise HTTPException(400, "Age must be positive")
    
    # Business logic
    prediction = model.predict(...)
    return prediction

# ✅ GOOD - Pydantic for structure, manual for logic
@app.post("/predict")
async def predict(data: UserInput):
    # Pydantic validated: type, range, format
    # data.age is guaranteed valid (0-150)
    
    # Manual check for business rules
    if data.age < 18:  # ← Business rule not in validator
        raise HTTPException(400, "Must be 18+")
    
    # Fetch from database
    try:
        db_user = await db.get_user(data.user_id)
        if not db_user:
            raise HTTPException(404, "User not found")
    except Exception as e:
        raise HTTPException(500, "Database error")
    
    # Prediction
    prediction = model.predict(...)
    return prediction

# Best pattern:
# 1. Pydantic validators: Type, format, basic rules
# 2. Endpoint logic: Business rules, DB checks, external calls
```

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
