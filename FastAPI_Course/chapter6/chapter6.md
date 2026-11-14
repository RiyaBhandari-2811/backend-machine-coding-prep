# Chapter 6: Machine Learning Model Serving with FastAPI

## Overview

Learn to serve machine learning models via REST APIs using FastAPI. This chapter covers the complete ML-to-API pipeline:

**3-Part Architecture:**
1. **Model Building** - Train and export ML model
2. **API Creation** - Serve model via FastAPI endpoint
3. **Frontend** - Consume API with Streamlit UI

---

## Problem Statement: Insurance Premium Prediction

### Use Case

Predict insurance premium category for customers based on personal attributes.

**Input Features (Raw Data from User):**
- Age (years)
- Weight (kg)
- Height (meters)
- Annual Income (LPA - Lakh Per Annum)
- Smoker (Yes/No)
- City (residence)
- Occupation (category)

**Output (Prediction):**
- Premium Category: **High** / **Medium** / **Low**

**Who Uses This?**
- Insurance companies: Segment customers for pricing
- Users: Understand their premium category upfront

---

## Part 1: Feature Engineering Strategy

### Why Feature Engineering?

Raw input features don't directly match model training features. We need to:
1. Compute derived features (BMI, age groups)
2. Encode categorical data
3. Create risk scores

### Feature Transformation

| Raw Input | Derived Feature | Logic |
|-----------|---|---|
| Weight, Height | **BMI** | weight / (height²) |
| Age | **Age Group** | Categorize: Young (0-25), Adult (25-45), Middle-aged (45-60), Senior (60+) |
| BMI, Smoker | **Lifestyle Risk** | High/Medium/Low based on BMI + smoker status |
| City | **City Tier** | Tier-1: Metro cities, Tier-2: Second tier, Tier-3: Other |
| Income | **Income (LPA)** | As-is (no transformation) |
| Occupation | **Occupation** | One-hot encoded |

### Risk Calculation

```
Lifestyle Risk:
- High: BMI > 30 AND Smoker = Yes
- Medium: BMI > 27 AND Smoker = Yes (OR) BMI > 30
- Low: BMI ≤ 25 OR Smoker = No
```

---

## Part 2: API Endpoint Design

### Challenge: User Input vs Model Input

**Problem:**
- User provides raw data (age, weight, height, etc.)
- Model expects processed features (BMI, age_group, lifestyle_risk, city_tier)
- We can't ask user to calculate BMI or categorize age

**Solution:**
- Accept raw input from user
- Compute all features server-side
- Pass processed features to model

### HTTP Method: POST

Why POST, not GET?
- **Broad Definition:** POST sends data to server for processing
- **Not just creation:** Can process, transform, or make predictions
- **ML Inference:** Common to use POST for model predictions

### Request Flow

```
1. Client sends POST /predict with raw user data
   ↓
2. Pydantic validates input
   ↓
3. Computed fields calculate: BMI, age_group, lifestyle_risk, city_tier
   ↓
4. Build feature dataframe matching model training format
   ↓
5. Model predicts: High/Medium/Low
   ↓
6. Return prediction as JSON (status 200)
```

### Pydantic Model with Computed Fields

```python
class UserInput(BaseModel):
    # Raw user input fields
    age: int
    weight: float
    height: float
    income_lpa: float
    smoker: bool
    city: str
    occupation: str
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        # Complex logic based on BMI + smoker
        ...
```

---

## Part 3: Model Export & Loading

### Pickle Serialization

**Export Model (in Jupyter):**
```python
import pickle

with open('model.pkl', 'wb') as f:
    pickle.dump(trained_pipeline, f)
```

**Load Model (in FastAPI):**
```python
import pickle

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
```

**Why Pickle?**
- Simple: One-liner to serialize
- Standard: Works with scikit-learn, XGBoost, etc.
- Binary: Smaller file size

**Alternatives:**
- ONNX: Cross-framework compatibility
- PMML: Interoperability format
- joblib: Better for large numpy arrays

---

## Inference Pipeline

### Step-by-Step Process

```python
# 1. Load model at startup
model = pickle.load(open('model.pkl', 'rb'))

# 2. Receive user input
user_data = UserInput(age=35, weight=79, height=1.72, ...)

# 3. Build feature dataframe
input_df = pd.DataFrame({
    'bmi': [user_data.bmi],
    'age_group': [user_data.age_group],
    'lifestyle_risk': [user_data.lifestyle_risk],
    'city_tier': [user_data.city_tier],
    'income_lpa': [user_data.income_lpa],
    'occupation': [user_data.occupation]
})

# 4. Make prediction
prediction = model.predict(input_df)[0]

# 5. Return result
return {"category": prediction}
```

### Why Computed Fields?

✅ **Single source of truth** - Calculate once, use everywhere  
✅ **Consistency** - Same logic for all users  
✅ **Simplicity** - User doesn't calculate BMI  
✅ **Validation** - Pydantic ensures correctness  

---

## Part 4: Streamlit Frontend

### Why Streamlit?

- **Fast:** Build UI without HTML/CSS/JS
- **Python:** Use Python for entire stack
- **Interactive:** Forms, buttons, inputs built-in
- **Deployment:** Easy to deploy (Streamlit Cloud)

### Components Used

```python
import streamlit as st
import requests

# 1. Title
st.title("Insurance Premium Predictor")

# 2. Number inputs
age = st.number_input("Age", min_value=0, max_value=100, value=30)
weight = st.number_input("Weight (kg)", min_value=20, value=70)
height = st.number_input("Height (m)", min_value=1.2, value=1.70)

# 3. Dropdown
smoker = st.selectbox("Are you a smoker?", ["No", "Yes"])

# 4. Button
if st.button("Predict Premium Category"):
    # Send to API
    response = requests.post("http://localhost:8000/predict", json={...})
    
    # Display result
    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Category: {result['category']}")
```

---

## Complete Architecture Diagram

```
┌─────────────────┐
│   Jupyter       │
│   Notebook      │
│  (Train Model)  │
└────────┬────────┘
         │ Export
         ↓
    model.pkl
         │
         ├──────────────────┐
         │                  │
         ↓                  ↓
    ┌──────────┐       ┌──────────┐
    │ FastAPI  │       │ Streamlit│
    │   API    │←─────→│ Frontend │
    │ (Backend)│       │  (UI)    │
    └──────────┘       └──────────┘
         ↑                  ↑
         │                  │
      :8000             :8501
```

---

## Interview Questions

**Q1: Why use POST for predictions instead of GET?**
A: POST sends complex data in request body. GET is for retrieving data, POST is for server processing.

**Q2: Why compute features server-side instead of client-side?**
A: Avoid asking users to calculate BMI/age groups. Simpler UX. Single source of truth.

**Q3: How do you export a scikit-learn model?**
A: `pickle.dump(model, open('model.pkl', 'wb'))`

**Q4: Why use Pydantic's computed fields?**
A: Automatically calculate derived features. Single place to define logic.

**Q5: What's the difference between model training and inference?**
A: Training: Learn patterns from data. Inference: Use learned model to predict on new data.

**Q6: Can you use the same Pydantic model for training and inference?**
A: No. Training model has all required fields. Inference model has optional fields for partial updates.

**Q7: Why pickle the model?**
A: Serialize Python object to binary file. Load it fast without retraining.

**Q8: What does `model.predict(X)` return?**
A: Array of predictions. For single sample: `model.predict(X)[0]`

**Q9: Can you serve multiple models from one API?**
A: Yes! Load multiple models, create multiple endpoints: `/predict/model1`, `/predict/model2`

**Q10: How do you handle model versioning?**
A: Store models as `model_v1.pkl`, `model_v2.pkl`. Load based on version query parameter.

---

## 🤔 Confusing Questions (Follow-Up Interview Questions)

### Q11: Can you load multiple different ML models simultaneously? What's the memory cost?

**Answer:**

YES, but each model consumes memory:

```python
import pickle

# Load multiple models at startup
model_v1 = pickle.load(open('model_v1.pkl', 'rb'))
model_v2 = pickle.load(open('model_v2.pkl', 'rb'))
model_v3 = pickle.load(open('model_v3.pkl', 'rb'))

@app.post("/predict")
async def predict(data: UserInput, version: int = 1):
    if version == 1:
        return model_v1.predict(...)
    elif version == 2:
        return model_v2.predict(...)
    # etc
```

**Memory considerations:**

```
model_v1: 50 MB
model_v2: 50 MB
model_v3: 50 MB
Total: 150 MB in memory

Prediction time: Fast (models already loaded)
Startup time: Slow (wait for all models to load)
Memory usage: High (all models stay in RAM)
```

**Alternatives:**

```python
# Load on-demand (lazy loading)
models = {}

def get_model(version):
    if version not in models:
        models[version] = pickle.load(open(f'model_v{version}.pkl', 'rb'))
    return models[version]

# Pros: Lower startup time
# Cons: First prediction with new version is slow
```

---

### Q12: What if the ML model prediction crashes? Does the entire API crash?

**Answer:**

NO! FastAPI handles exceptions gracefully:

```python
@app.post("/predict")
async def predict_premium(data: UserInput):
    try:
        predictions = model.predict(...)
        return {"premium": predictions[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        # API returns 500 error, but doesn't crash
        # Can handle next request normally
```

**What CAN crash the API:**

```python
# ❌ Loading model crashes at startup
@app.on_event("startup")
async def startup():
    global model
    model = pickle.load(open('nonexistent.pkl'))  # ← Crashes here!
    # API never starts!

# Solution: Use try-except at startup too
@app.on_event("startup")
async def startup():
    global model
    try:
        model = pickle.load(open('model.pkl', 'rb'))
    except Exception as e:
        print(f"Warning: Model loading failed: {e}")
        model = None  # Use default model or None
```

---

### Q13: Can you use a Tensorflow/PyTorch model directly, or must it be pickled?

**Answer:**

Both work, but pickling is simpler:

```python
# ✅ Pickled model (simpler)
import pickle
model = pickle.load(open('model.pkl', 'rb'))

# ✅ TensorFlow model
import tensorflow as tf
model = tf.keras.models.load_model('model.h5')

# ✅ PyTorch model
import torch
model = torch.load('model.pth')

# ✅ Scikit-learn model (native pickle support)
from joblib import load  # Better than pickle for sklearn!
model = load('model.joblib')
```

**Comparison:**

| Format | Pros | Cons |
|--------|------|------|
| Pickle | Simple, Python native | Not cross-language |
| TensorFlow | Production-ready | Large file size |
| PyTorch | GPU support | Slower startup |
| Joblib | sklearn optimized | sklearn-specific |

**Best practice:**

```python
# For scikit-learn: Use joblib
from joblib import load
model = load('model.joblib')  # Better than pickle!

# For TensorFlow: Use native format
model = tf.keras.models.load_model('model')

# For PyTorch: Use torch.load
model = torch.load('model.pth')
```

---

### Q14: What happens if the model pickled file is corrupted? Can you validate it before using?

**Answer:**

Pickle loads corrupt files and crashes:

```python
# ❌ No validation
model = pickle.load(open('model.pkl', 'rb'))
# If file is corrupted → UnpicklingError

# ✅ With validation
import pickle
import os

def load_model_safely(filepath):
    # Check file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model file not found: {filepath}")
    
    # Check file size (sanity check)
    size = os.path.getsize(filepath)
    if size < 1000:  # Less than 1KB is suspicious
        raise ValueError(f"Model file too small: {size} bytes")
    
    try:
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        return model
    except (pickle.UnpicklingError, EOFError) as e:
        raise ValueError(f"Failed to load model: {e}")
    except Exception as e:
        raise ValueError(f"Unexpected error loading model: {e}")

# Usage
try:
    model = load_model_safely('model.pkl')
except ValueError as e:
    print(f"Error: {e}")
    # Use backup model or return error to user
```

---

### Q15: Can you use GET for predictions if the input is simple (not complex)?

**Answer:**

Technically yes, but it's BAD PRACTICE:

```python
# ❌ BAD - Using GET for predictions
@app.get("/predict")
async def predict(age: int, weight: float, height: float):
    result = model.predict([[age, weight, height]])
    return {"prediction": result[0]}

# URL: /predict?age=30&weight=75&height=1.8
# Problem: URL gets very long for many features
# Problem: Data visible in browser history
# Problem: Breaks REST convention (GET shouldn't process/modify)


# ✅ GOOD - Using POST
@app.post("/predict")
async def predict(data: UserInput):
    result = model.predict([data.model_dump()])
    return {"prediction": result[0]}

# Request body: {...}
# Better: Private, organized, RESTful
```

**When GET might make sense:**

```python
# GET for simple cached queries
@app.get("/model-info")
async def get_model_info():
    return {
        "version": "v1.0",
        "accuracy": 0.95,
        "features": ["age", "weight", "height"]
    }
```

---

### Q16: What if the model requires feature scaling (normalization) but you forget to apply it?

**Answer:**

Model will give WRONG predictions:

```python
# Training data was scaled (-1 to 1)
# Test data NOT scaled (0 to 100)
# Model learns patterns in scaled space
# Makes predictions on unscaled data
# → GARBAGE predictions!

# ✅ Correct approach
from sklearn.preprocessing import StandardScaler
import pickle

# During training
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
model.fit(X_train_scaled, y_train)

# Save both model AND scaler
pickle.dump((model, scaler), open('model.pkl', 'wb'))

# During inference
model, scaler = pickle.load(open('model.pkl', 'rb'))

@app.post("/predict")
async def predict(data: UserInput):
    # Scale input before prediction!
    features = [[data.age, data.weight, data.height]]
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)
    return {"prediction": prediction[0]}
```

**Common mistake:**

```python
# ❌ Save only model, forget scaler
pickle.dump(model, open('model.pkl', 'wb'))

# Later, inference without scaling
# → Wrong predictions!

# ✅ Save both together
state = {'model': model, 'scaler': scaler}
pickle.dump(state, open('model.pkl', 'wb'))

# Later, load both
state = pickle.load(open('model.pkl', 'rb'))
model = state['model']
scaler = state['scaler']
```

---

### Q17: How do you prevent the API from serving stale predictions from a cached model?

**Answer:**

Problem: If model is retrained, old model is still in memory:

```python
# Model loaded at startup
@app.on_event("startup")
async def startup():
    global model
    model = pickle.load(open('model.pkl', 'rb'))

# If model.pkl is updated on disk
# Old model stays in memory!
# API serves stale predictions!

# ✅ Solution 1: Reload on each request (slow)
@app.post("/predict")
async def predict(data: UserInput):
    model = pickle.load(open('model.pkl', 'rb'))  # Load fresh
    prediction = model.predict(...)
    return {"prediction": prediction[0]}

# ✅ Solution 2: Check file modification time
import os
import time

last_modified = 0

def get_model():
    global model, last_modified
    current_modified = os.path.getmtime('model.pkl')
    if current_modified != last_modified:
        model = pickle.load(open('model.pkl', 'rb'))
        last_modified = current_modified
    return model

@app.post("/predict")
async def predict(data: UserInput):
    current_model = get_model()  # Loads fresh if updated
    prediction = current_model.predict(...)
    return {"prediction": prediction[0]}

# ✅ Solution 3: Model versioning endpoint
@app.post("/predict")
async def predict(data: UserInput, version: str = "latest"):
    model = pickle.load(open(f'models/model_{version}.pkl', 'rb'))
    prediction = model.predict(...)
    return {"prediction": prediction[0]}

# Usage: /predict?version=v2.1 (get specific version)
```

---

### Q18: Can the Pydantic model do feature engineering (like creating new features)?

**Answer:**

YES! Using computed fields:

```python
from pydantic import BaseModel, computed_field
import math

class UserInput(BaseModel):
    age: int
    weight: float
    height: float
    income: float
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 30:
            return "young"
        elif self.age < 60:
            return "middle"
        else:
            return "senior"
    
    @computed_field
    @property
    def income_per_year(self) -> float:
        return self.income * 12
    
    @computed_field
    @property
    def log_income(self) -> float:
        return math.log(self.income + 1)

# All features computed automatically!
user = UserInput(age=35, weight=75, height=1.75, income=5000)
features = user.model_dump()
# {age: 35, weight: 75, height: 1.75, income: 5000, bmi: 24.5, age_group: "middle", ...}

# Pass to model
X = [[features['age'], features['bmi'], features['age_group']]]
prediction = model.predict(X)
```

---

### Q19: What's the performance difference between sync and async endpoints for predictions?

**Answer:**

Async is better for CONCURRENT requests:

```python
# ❌ Sync endpoint (blocks)
@app.post("/predict")
def predict_sync(data: UserInput):
    prediction = model.predict(...)
    return {"prediction": prediction}

# If 10 requests come simultaneously:
# Request 1: Predicts (2 seconds) → blocks others
# Request 2: Waits (can't predict yet)
# Request 3: Waits (can't predict yet)
# Total time: 20 seconds (10 requests × 2 seconds each)


# ✅ Async endpoint (non-blocking)
@app.post("/predict")
async def predict_async(data: UserInput):
    prediction = model.predict(...)  # Assume 2 seconds
    return {"prediction": prediction}

# If 10 requests come simultaneously:
# Requests 1-10: All start predicting "concurrently"
# Since prediction is CPU-bound, still takes ~2 seconds total (but handled together)
# Total time: ~2 seconds (all 10 requests in parallel)
```

**BUT: ML predictions are usually CPU-bound (not I/O-bound)!**

```python
# CPU-bound prediction
prediction = model.predict(X)  # Takes 100% CPU for 2 seconds
# Async doesn't help much here (still blocking CPU)

# I/O-bound operation
result = await database.query()  # Async helps (non-blocking wait)
```

**Best practice:**

```python
# Use async for I/O operations
@app.post("/predict")
async def predict(data: UserInput):
    # Async: Log to async database
    await db.insert_log(data)
    
    # Sync: CPU-bound prediction
    prediction = model.predict(...)  # Still blocking, but OK
    
    return {"prediction": prediction}

# For better concurrency with CPU-bound, use:
# - Multiple workers (Gunicorn)
# - Process pools (ProcessPoolExecutor)
# - Distributed inference (Ray, Dask)
```

---

### Q20: Can you serve predictions without the model? What if model loading fails?

**Answer:**

YES! Use a default/fallback model:

```python
# Load with fallback
model = None

@app.on_event("startup")
async def startup():
    global model
    try:
        model = pickle.load(open('model.pkl', 'rb'))
    except Exception as e:
        print(f"Warning: Failed to load model: {e}")
        model = None  # Use default

@app.post("/predict")
async def predict(data: UserInput):
    if model is None:
        # Use default prediction logic
        return {
            "prediction": "unknown",
            "confidence": 0.0,
            "warning": "Model not loaded, using default"
        }
    
    # Use actual model
    prediction = model.predict(...)
    return {"prediction": prediction[0]}
```

**Strategies:**

```python
# Strategy 1: Always have a fallback
DEFAULT_PREDICTION = 0.5

# Strategy 2: Return 503 Service Unavailable
if model is None:
    raise HTTPException(503, "Model not ready")

# Strategy 3: Use backup model
try:
    model = pickle.load(open('model.pkl', 'rb'))
except:
    model = pickle.load(open('model_backup.pkl', 'rb'))

# Strategy 4: Health check endpoint
@app.get("/health")
async def health_check():
    return {"model_loaded": model is not None}

# Client can check health before making predictions
```

---

## Deployment Considerations

### Local Development
```bash
# Terminal 1: Start FastAPI
uvicorn main:app --reload --port 8000

# Terminal 2: Start Streamlit
streamlit run frontend.py --server.port 8501
```

### Production Deployment

**API Server (FastAPI):**
- Use Gunicorn/Uvicorn
- Run behind Nginx/load balancer
- Container with Docker
- Deploy to: AWS, GCP, Azure, Heroku

**Frontend (Streamlit):**
- Streamlit Community Cloud (simplest)
- Docker container
- Same cloud provider as API

### CORS (Cross-Origin Request)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Performance Optimization

### Batch Predictions

```python
@app.post("/predict-batch")
def predict_batch(users: List[UserInput]):
    # Process multiple users at once
    input_df = pd.DataFrame([u.model_dump() for u in users])
    predictions = model.predict(input_df)
    return {"predictions": predictions.tolist()}
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1)
def load_model():
    return pickle.load(open('model.pkl', 'rb'))
```

### Async Processing

```python
@app.post("/predict")
async def predict_premium(data: UserInput):
    # Async endpoint for better concurrency
    ...
```

---

## Summary

✅ **3-Part Pipeline**
- Model Building (scikit-learn, pickle)
- API Creation (FastAPI + Pydantic)
- Frontend (Streamlit)

✅ **Feature Engineering**
- Server-side computation
- Computed fields for derived features
- Transformation pipeline

✅ **User Flow**
- User enters raw data in Streamlit UI
- Data sent to FastAPI endpoint via POST
- Endpoint processes, validates, predicts
- Result returned as JSON
- Streamlit displays prediction

✅ **Best Practices**
- Separate frontend and backend
- Validate inputs with Pydantic
- Pickle model for easy serialization
- Use computed fields for feature logic
- Add CORS for cross-origin requests

---

## Next Steps

- Deploy to production
- Add model versioning
- Implement batch predictions
- Monitor inference latency
- A/B test different models

👉 Start with `main.py` to see complete implementation!
