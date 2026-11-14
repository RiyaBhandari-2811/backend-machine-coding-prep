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
