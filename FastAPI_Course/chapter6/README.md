# Chapter 6: Machine Learning Model Serving - Quick Start Guide

## 📚 Chapter Overview

**Chapter 6** is the culmination of the FastAPI course, demonstrating a **complete real-world ML-to-API pipeline**.

### 3-Part Architecture

```
Part 1: Model Building
┌─────────────────────────────┐
│ Train ML Model              │
│ (Insurance Premium)         │
│ Input: age, weight, height, │
│        income, smoker, etc. │
│ Output: High/Medium/Low     │
└────────────┬────────────────┘
             │ Export
             ▼
        model.pkl

Part 2: API Backend
┌─────────────────────────────┐
│ FastAPI Server              │
│ - Load model                │
│ - Validate input            │
│ - Compute features          │
│ - Make predictions          │
│ - Return JSON               │
└──────────┬──────────────────┘
           │
        :8000

Part 3: Frontend
┌─────────────────────────────┐
│ Streamlit UI                │
│ - Form input                │
│ - Call API                  │
│ - Display results           │
│ - Show explanations         │
└─────────────────────────────┘
           │
        :8501
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd chapter6
pip install -r requirements.txt
```

**Dependencies:**
- `fastapi==0.104.1` - Web framework
- `uvicorn==0.24.0` - ASGI server
- `pydantic==2.5.0` - Data validation
- `pandas==2.1.3` - Data manipulation
- `scikit-learn==1.3.2` - ML models
- `streamlit==1.29.0` - Frontend UI
- `requests==2.31.0` - HTTP client

### 2. Start FastAPI Backend (Terminal 1)

```bash
# Make sure you're in chapter6 directory
cd chapter6

# Start the server
uvicorn main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Check API:**
- Visit: http://localhost:8000/docs
- Swagger UI interactive documentation

### 3. Start Streamlit Frontend (Terminal 2)

```bash
cd chapter6

# Start the UI
streamlit run frontend.py --server.port 8501
```

**Expected output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### 4. Use the Application

1. Open browser: http://localhost:8501
2. Fill in personal information:
   - Age: 35
   - Weight: 79 kg
   - Height: 1.72 m
   - Income: 10 LPA
   - Smoker: No
   - City: Gurgaon
   - Occupation: Software Engineer
3. Click "🔮 Predict Premium Category"
4. View prediction: **Low** / **Medium** / **High**

---

## 📁 File Structure

```
chapter6/
├── chapter6.md          (412 lines) - Complete guide
├── main.py              (698 lines) - FastAPI backend
├── frontend.py          (383 lines) - Streamlit UI
├── requirements.txt     (7 lines)   - Dependencies
└── model.pkl            (optional)  - Pre-trained model
```

### chapter6.md

**Comprehensive guide covering:**
- Problem statement (Insurance Premium Prediction)
- Feature engineering strategy
- API endpoint design
- Model export & loading
- Complete inference pipeline
- Streamlit components
- Deployment considerations
- 10 Interview Q&A

**Lines:** 412

### main.py

**FastAPI backend with:**
- Model loading (pickle)
- Pydantic models with computed fields:
  - `UserInput` - Raw user data validation
  - `PredictionResponse` - Structured response
- 3 endpoints:
  - `POST /predict` - Single prediction
  - `POST /predict-batch` - Multiple predictions
  - `GET /explain/{user_id}` - Feature explanation
- CORS middleware for frontend
- Error handling
- Full documentation

**Features:**
- ✅ BMI computation
- ✅ Age group categorization
- ✅ Lifestyle risk assessment
- ✅ City tier classification
- ✅ JSON validation and response

**Lines:** 698

### frontend.py

**Streamlit frontend with:**
- Page configuration
- Sidebar settings
- Input form (7 fields)
- API communication
- Result display with color coding
- Factor analysis (table & detailed views)
- Recommendations based on prediction
- Error handling
- Debug mode

**Features:**
- 🎨 Responsive layout
- 📊 Data visualization
- 💡 Smart recommendations
- 🐛 Debug mode
- 🔐 Privacy notice

**Lines:** 383

---

## 🔧 Testing the API

### Test with Swagger UI (Recommended)

1. Go to: http://localhost:8000/docs
2. Find POST `/predict` endpoint
3. Click "Try it out"
4. Enter example data:
```json
{
  "age": 35,
  "weight": 79,
  "height": 1.72,
  "income_lpa": 10,
  "smoker": false,
  "city": "Gurgaon",
  "occupation": "Software Engineer"
}
```
5. Click "Execute"
6. See response with prediction and explanation

### Test with cURL

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "weight": 79,
    "height": 1.72,
    "income_lpa": 10,
    "smoker": false,
    "city": "Gurgaon",
    "occupation": "Software Engineer"
  }'
```

### Test with Python

```python
import requests

url = "http://localhost:8000/predict"
data = {
    "age": 35,
    "weight": 79,
    "height": 1.72,
    "income_lpa": 10,
    "smoker": False,
    "city": "Gurgaon",
    "occupation": "Software Engineer"
}

response = requests.post(url, json=data)
print(response.json())
```

---

## 📊 Example Predictions

### Example 1: Low Premium (Healthy, Young Professional)

**Input:**
```json
{
  "age": 28,
  "weight": 70,
  "height": 1.75,
  "income_lpa": 15,
  "smoker": false,
  "city": "Bangalore",
  "occupation": "Software Engineer"
}
```

**Output:**
```json
{
  "predicted_category": "Low",
  "confidence_factors": {
    "age_group": "Adult",
    "lifestyle_risk": "Low",
    "bmi": 22.86,
    "city_tier": 1,
    "income_lpa": 15,
    "occupation": "Software Engineer"
  },
  "explanation": "Your premium is Low based on young age, low lifestyle risk. You qualify for lower premium rates!"
}
```

**Analysis:** Young, healthy BMI, non-smoker → Low risk

---

### Example 2: Medium Premium (Middle-aged, Overweight)

**Input:**
```json
{
  "age": 45,
  "weight": 85,
  "height": 1.72,
  "income_lpa": 25,
  "smoker": false,
  "city": "Delhi",
  "occupation": "Doctor"
}
```

**Output:**
```json
{
  "predicted_category": "Medium",
  "confidence_factors": {
    "age_group": "Middle-aged",
    "lifestyle_risk": "Low",
    "bmi": 28.74,
    "city_tier": 1,
    "income_lpa": 25,
    "occupation": "Doctor"
  },
  "explanation": "Your premium is Medium based on middle-aged, overweight. Consider lifestyle changes to reduce premium."
}
```

**Analysis:** Middle-aged, overweight (BMI > 25) → Medium risk

---

### Example 3: High Premium (Senior, Smoker, Obese)

**Input:**
```json
{
  "age": 65,
  "weight": 95,
  "height": 1.70,
  "income_lpa": 5,
  "smoker": true,
  "city": "Mumbai",
  "occupation": "Retired"
}
```

**Output:**
```json
{
  "predicted_category": "High",
  "confidence_factors": {
    "age_group": "Senior",
    "lifestyle_risk": "High",
    "bmi": 32.87,
    "city_tier": 1,
    "income_lpa": 5,
    "occupation": "Retired"
  },
  "explanation": "Your premium is High based on senior age, high lifestyle risk (smoker + high BMI), lower income bracket. Consider lifestyle changes to reduce premium."
}
```

**Analysis:** Senior age, obese (BMI > 30), smoker → High risk

---

## 🎯 Key Concepts Demonstrated

### 1. **Feature Engineering**
- Compute BMI from weight and height
- Categorize age into groups
- Assess lifestyle risk
- Classify cities into tiers

### 2. **Pydantic Computed Fields**
```python
@computed_field
@property
def bmi(self) -> float:
    return round(self.weight / (self.height ** 2), 2)
```

### 3. **Model Serving**
- Load pickle model at startup
- Create dataframe matching training format
- Make predictions
- Return structured JSON

### 4. **API Design**
- POST for data processing (not just creation)
- Proper status codes (200, 400, 500)
- CORS for cross-origin requests
- Error handling with meaningful messages

### 5. **Frontend-Backend Communication**
- HTTP requests with requests library
- JSON serialization/deserialization
- Error handling and timeouts
- User-friendly result display

---

## 🏆 Complete FastAPI Course Status

```
✅ Chapter 1: FastAPI Fundamentals (750 lines)
✅ Chapter 2: HTTP Methods & CRUD (950 lines)
✅ Chapter 3: Path/Query Parameters (950 lines)
✅ Chapter 4: POST Endpoint - CREATE (820 lines)
✅ Chapter 5: PUT/DELETE - Complete CRUD (852 lines)
✅ Chapter 6: ML Model Serving (1,500 lines) ← YOU ARE HERE

Total: 6 chapters, 6,622 lines of code + documentation
```

---

## 💡 Interview Questions

**Q: Why use POST for ML predictions instead of GET?**
A: POST is for server-side processing. GET is for retrieving data. Predictions require computation.

**Q: How do computed fields help?**
A: They automatically calculate derived features from raw input. Single source of truth.

**Q: What's the benefit of feature engineering server-side?**
A: Don't burden users. Simpler UX. Consistent logic. Security (users can't manipulate features).

**Q: How do you export a trained model?**
A: `pickle.dump(model, open('model.pkl', 'wb'))`

**Q: Can you serve multiple models?**
A: Yes! Load multiple models, create multiple endpoints: `/predict/model1`, `/predict/model2`

**Q: How to handle model versioning?**
A: Store as `model_v1.pkl`, `model_v2.pkl`. Load based on version parameter.

---

## 🚀 Next Steps

### Production Deployment

1. **Containerize with Docker:**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

2. **Deploy to Cloud:**
   - AWS: ECS, Lambda, SageMaker
   - GCP: Cloud Run, App Engine
   - Azure: Container Instances
   - Heroku: Simple deployment

3. **Add Monitoring:**
   - Log predictions
   - Track latency
   - Monitor model performance
   - Alert on anomalies

4. **Scale:**
   - Load balancer
   - Multiple API replicas
   - Caching layer (Redis)
   - CDN for frontend

---

## 📖 Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Scikit-learn ML Models](https://scikit-learn.org/)

---

**Happy coding! 🎉**
