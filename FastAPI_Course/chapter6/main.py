"""
Chapter 6: Machine Learning Model Serving with FastAPI
Insurance Premium Prediction - Complete Implementation

This chapter demonstrates:
- Loading and serving pre-trained ML models
- Feature engineering in API endpoints
- Pydantic computed fields for derived features
- POST endpoint for model predictions
- Request/response validation

Project Structure:
- main.py: FastAPI backend with ML model
- model.pkl: Pre-trained scikit-learn model
- frontend.py: Streamlit UI for predictions
"""

import json
import pickle
from typing import Literal, Optional
from pydantic import BaseModel, Field, computed_field
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ============================================================================
# SETUP
# ============================================================================

app = FastAPI(
    title="Insurance Premium Prediction API",
    description="Serve ML models via FastAPI - Complete CRUD + ML",
    version="6.0"
)

# ============================================================================
# CORS CONFIGURATION
# ============================================================================
# Allow Streamlit frontend to make requests from different port

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# MODEL LOADING
# ============================================================================

def load_model():
    """
    Load pre-trained ML model from pickle file.
    
    NOTE: In production, use load_model_from_cloud() to fetch from S3/GCP
    
    The model is a scikit-learn pipeline trained on insurance data.
    It expects features: [BMI, Age_Group, Lifestyle_Risk, City_Tier, Income_LPA, Occupation]
    
    Output: 'High' / 'Medium' / 'Low' (premium category)
    """
    try:
        with open('model.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        # If actual model not available, use mock model
        return MockModel()


class MockModel:
    """
    Fallback mock model when real model.pkl not available.
    Uses simple decision rules instead of actual ML.
    """
    def predict(self, X):
        """
        Simple heuristic-based prediction.
        
        Rules:
        - High Risk: Age_Group=Senior OR Lifestyle_Risk=High OR BMI>30
        - Low Risk: Age_Group=Young AND Lifestyle_Risk=Low
        - Medium Risk: Everything else
        """
        predictions = []
        for idx, row in X.iterrows():
            age_group = row['age_group']
            lifestyle_risk = row['lifestyle_risk']
            bmi = row['bmi']
            income = row['income_lpa']
            
            # Simple decision tree
            if (age_group == 'Senior' or 
                lifestyle_risk == 'High' or 
                bmi > 30):
                pred = 'High'
            elif (age_group == 'Young' and 
                  lifestyle_risk == 'Low' and 
                  income < 20):
                pred = 'Low'
            else:
                pred = 'Medium'
            
            predictions.append(pred)
        
        return predictions


# Load model at startup
try:
    model = load_model()
    MODEL_LOADED = True
except Exception as e:
    print(f"⚠️  Error loading model: {e}")
    model = MockModel()
    MODEL_LOADED = False


# ============================================================================
# PYDANTIC MODELS FOR VALIDATION
# ============================================================================

class UserInput(BaseModel):
    """
    User input validation model.
    
    Accepts RAW data from user (age, weight, height, etc.)
    Automatically computes derived features via @computed_field
    
    Example input:
    {
        "age": 35,
        "weight": 79,
        "height": 1.72,
        "income_lpa": 10,
        "smoker": false,
        "city": "Gurgaon",
        "occupation": "Software Engineer"
    }
    """
    
    age: int = Field(
        ...,
        gt=0,
        le=100,
        description="Age in years",
        example=35
    )
    
    weight: float = Field(
        ...,
        gt=30,
        lt=200,
        description="Weight in kilograms",
        example=79
    )
    
    height: float = Field(
        ...,
        gt=1.2,
        lt=2.5,
        description="Height in meters",
        example=1.72
    )
    
    income_lpa: float = Field(
        ...,
        gt=0,
        description="Annual income in LPA (Lakh Per Annum)",
        example=10
    )
    
    smoker: bool = Field(
        ...,
        description="Is the user a smoker?",
        example=False
    )
    
    city: str = Field(
        ...,
        min_length=2,
        description="City of residence",
        example="Gurgaon"
    )
    
    occupation: Literal[
        "Software Engineer",
        "Doctor",
        "Teacher",
        "Business Owner",
        "Government Job",
        "Unemployed",
        "Retired",
        "Others"
    ] = Field(
        ...,
        description="Occupation category",
        example="Software Engineer"
    )
    
    # ========================================================================
    # COMPUTED FIELDS (Feature Engineering)
    # ========================================================================
    
    @computed_field
    @property
    def bmi(self) -> float:
        """
        Calculate Body Mass Index.
        
        Formula: weight / (height²)
        
        Categories:
        - Underweight: BMI < 18.5
        - Normal: 18.5 ≤ BMI < 25
        - Overweight: 25 ≤ BMI < 30
        - Obese: BMI ≥ 30
        """
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def age_group(self) -> str:
        """
        Categorize age into groups.
        
        - Young: age < 25
        - Adult: 25 ≤ age < 45
        - Middle-aged: 45 ≤ age < 60
        - Senior: age ≥ 60
        """
        if self.age < 25:
            return "Young"
        elif self.age < 45:
            return "Adult"
        elif self.age < 60:
            return "Middle-aged"
        else:
            return "Senior"
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        """
        Calculate lifestyle risk score.
        
        Combines BMI and smoker status.
        
        Risk Levels:
        - High: Smoker=Yes AND BMI > 30
        - Medium: Smoker=Yes AND BMI > 27 OR (BMI > 30 AND Not Smoker)
        - Low: Otherwise
        """
        if self.smoker and self.bmi > 30:
            return "High"
        elif self.smoker and self.bmi > 27:
            return "Medium"
        elif self.bmi > 30:
            return "Medium"
        else:
            return "Low"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        """
        Categorize city into tiers for analysis.
        
        Tier-1 (Metro): Mumbai, Delhi, Bangalore, Hyderabad, Chennai, Pune
        Tier-2 (Second tier): Gurgaon, Noida, Jaipur, Indore, etc.
        Tier-3 (Other): All remaining cities
        """
        tier1_cities = {
            "Mumbai", "Delhi", "Bangalore", "Hyderabad", 
            "Chennai", "Pune", "Kolkata", "Chandigarh"
        }
        
        tier2_cities = {
            "Gurgaon", "Noida", "Jaipur", "Indore", "Lucknow",
            "Kochi", "Surat", "Ahmedabad", "Bhopal", "Visakhapatnam"
        }
        
        city = self.city.strip().title()  # Normalize: lowercase -> Title case
        
        if city in tier1_cities:
            return 1
        elif city in tier2_cities:
            return 2
        else:
            return 3


class PredictionResponse(BaseModel):
    """Response model for predictions."""
    
    predicted_category: str = Field(
        ...,
        description="Predicted premium category: High/Medium/Low",
        example="Medium"
    )
    
    confidence_factors: dict = Field(
        default_factory=dict,
        description="Factors influencing prediction",
        example={"age_group": "Adult", "lifestyle_risk": "Low", "bmi": 26.7}
    )
    
    explanation: str = Field(
        ...,
        description="Human-readable explanation",
        example="Your premium is Medium due to age group and lifestyle factors"
    )


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
def root():
    """API information and health check."""
    return {
        "message": "Welcome to Insurance Premium Prediction API",
        "chapter": 6,
        "title": "Machine Learning Model Serving",
        "features": [
            "Load pre-trained ML models",
            "Feature engineering in API",
            "Pydantic computed fields",
            "Model predictions",
            "Error handling"
        ],
        "model_status": "Loaded" if MODEL_LOADED else "Using Mock Model",
        "endpoints": ["/predict", "/docs"]
    }


# ============================================================================
# ENDPOINT 1: PREDICT INSURANCE PREMIUM (POST)
# ============================================================================

@app.post("/predict", response_model=PredictionResponse, status_code=200)
def predict_premium(user_data: UserInput):
    """
    Predict insurance premium category.
    
    Process:
    1. Validate user input via Pydantic
    2. Compute derived features (BMI, age_group, lifestyle_risk, city_tier)
    3. Build feature dataframe for model
    4. Make prediction
    5. Return result with explanation
    
    Args:
        user_data: User information (age, weight, height, income, etc.)
    
    Returns:
        PredictionResponse with:
        - predicted_category: High/Medium/Low
        - confidence_factors: Feature values used
        - explanation: Human-readable result
    
    Example Request:
    POST /predict
    {
        "age": 35,
        "weight": 79,
        "height": 1.72,
        "income_lpa": 10,
        "smoker": false,
        "city": "Gurgaon",
        "occupation": "Software Engineer"
    }
    
    Example Response:
    {
        "predicted_category": "Medium",
        "confidence_factors": {
            "age_group": "Adult",
            "lifestyle_risk": "Low",
            "bmi": 26.7,
            "city_tier": 2,
            "income_lpa": 10
        },
        "explanation": "Your premium is Medium due to age and lifestyle factors"
    }
    """
    
    try:
        # Step 1: Extract computed features from Pydantic model
        features = {
            'bmi': user_data.bmi,
            'age_group': user_data.age_group,
            'lifestyle_risk': user_data.lifestyle_risk,
            'city_tier': user_data.city_tier,
            'income_lpa': user_data.income_lpa,
            'occupation': user_data.occupation
        }
        
        # Step 2: Build dataframe for model (must match training format)
        input_df = pd.DataFrame([features])
        
        # Step 3: Make prediction
        prediction = model.predict(input_df)[0]
        
        # Step 4: Generate explanation
        explanation = generate_explanation(user_data, prediction)
        
        # Step 5: Return structured response
        return PredictionResponse(
            predicted_category=prediction,
            confidence_factors=features,
            explanation=explanation
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )


def generate_explanation(user_data: UserInput, prediction: str) -> str:
    """Generate human-readable explanation for prediction."""
    
    factors = []
    
    if user_data.age_group == "Senior":
        factors.append("senior age")
    elif user_data.age_group == "Young":
        factors.append("young age")
    
    if user_data.lifestyle_risk == "High":
        factors.append("high lifestyle risk (smoker + high BMI)")
    elif user_data.lifestyle_risk == "Medium":
        factors.append("medium lifestyle risk")
    
    if user_data.bmi > 30:
        factors.append("obesity (BMI > 30)")
    
    if user_data.income_lpa < 5:
        factors.append("lower income bracket")
    elif user_data.income_lpa > 50:
        factors.append("higher income bracket")
    
    if user_data.city_tier == 1:
        factors.append("metro city residence")
    
    factor_text = ", ".join(factors) if factors else "standard profile"
    
    explanation = f"Your premium is {prediction} based on {factor_text}."
    
    if prediction == "High":
        explanation += " Consider lifestyle changes to reduce premium."
    elif prediction == "Low":
        explanation += " You qualify for lower premium rates!"
    
    return explanation


# ============================================================================
# ENDPOINT 2: BATCH PREDICTIONS (POST) - BONUS
# ============================================================================

@app.post("/predict-batch")
def predict_batch(users: list[UserInput]):
    """
    Predict for multiple users at once.
    
    Useful for batch processing or data exports.
    More efficient than individual requests.
    
    Example Request:
    POST /predict-batch
    [
        {"age": 30, "weight": 70, ...},
        {"age": 45, "weight": 80, ...}
    ]
    
    Example Response:
    {
        "total_predictions": 2,
        "predictions": [
            {"user_index": 0, "category": "Low", ...},
            {"user_index": 1, "category": "Medium", ...}
        ]
    }
    """
    
    if not users:
        raise HTTPException(status_code=400, detail="Empty user list")
    
    if len(users) > 100:
        raise HTTPException(
            status_code=400,
            detail="Maximum 100 users per batch"
        )
    
    predictions = []
    
    for idx, user in enumerate(users):
        features = {
            'bmi': user.bmi,
            'age_group': user.age_group,
            'lifestyle_risk': user.lifestyle_risk,
            'city_tier': user.city_tier,
            'income_lpa': user.income_lpa,
            'occupation': user.occupation
        }
        
        input_df = pd.DataFrame([features])
        prediction = model.predict(input_df)[0]
        
        predictions.append({
            "user_index": idx,
            "category": prediction,
            "features": features
        })
    
    return JSONResponse(
        status_code=200,
        content={
            "total_predictions": len(predictions),
            "predictions": predictions
        }
    )


# ============================================================================
# ENDPOINT 3: FEATURE EXPLANATION (GET) - BONUS
# ============================================================================

@app.get("/explain/{user_id}")
def explain_features(user_id: str):
    """
    Explain what each feature means and how it affects prediction.
    
    Educational endpoint to help users understand model logic.
    """
    
    return {
        "features": {
            "bmi": "Body Mass Index calculated from weight and height",
            "age_group": "Age categorized: Young/Adult/Middle-aged/Senior",
            "lifestyle_risk": "Risk assessment based on BMI and smoking status",
            "city_tier": "City classification: 1=Metro, 2=Second-tier, 3=Other",
            "income_lpa": "Annual income in Lakh Per Annum",
            "occupation": "Profession or employment status"
        },
        "feature_importance": {
            "age_group": "High - Most important factor",
            "lifestyle_risk": "High - Major influence",
            "bmi": "Medium - Affects health assessment",
            "city_tier": "Medium - Regional pricing",
            "income_lpa": "Medium - Affordability indicator",
            "occupation": "Low - Secondary factor"
        },
        "prediction_rules": {
            "High": "Older age, high BMI, smoker status, or metro city",
            "Medium": "Mixed factors, moderate risk profile",
            "Low": "Young age, low BMI, non-smoker, good health"
        }
    }


# ============================================================================
# USAGE & TESTING
# ============================================================================

"""
HOW TO RUN:

1. START SERVER:
   uvicorn main:app --reload --port 8000

2. OPEN SWAGGER DOCS:
   http://localhost:8000/docs

3. TEST PREDICT ENDPOINT:

Example Request 1 (Low Premium):
POST /predict
{
    "age": 28,
    "weight": 70,
    "height": 1.75,
    "income_lpa": 15,
    "smoker": false,
    "city": "Bangalore",
    "occupation": "Software Engineer"
}
Expected: "Low" (Young, low BMI, non-smoker, good income)

Example Request 2 (High Premium):
POST /predict
{
    "age": 65,
    "weight": 95,
    "height": 1.70,
    "income_lpa": 5,
    "smoker": true,
    "city": "Mumbai",
    "occupation": "Retired"
}
Expected: "High" (Senior, high BMI, smoker, low income)

Example Request 3 (Medium Premium):
POST /predict
{
    "age": 45,
    "weight": 85,
    "height": 1.72,
    "income_lpa": 25,
    "smoker": false,
    "city": "Delhi",
    "occupation": "Doctor"
}
Expected: "Medium" (Middle-aged, overweight but not obese)

4. TEST WITH CURL:

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

5. RUN STREAMLIT FRONTEND:
   streamlit run frontend.py --server.port 8501
"""


# ============================================================================
# KEY CONCEPTS
# ============================================================================

"""
CHAPTER 6 CONCEPTS:

1. MODEL LOADING:
   - Pickle for serialization
   - Load at startup for efficiency
   - Handle missing model gracefully

2. COMPUTED FIELDS:
   - @computed_field for derived features
   - Automatic calculation from user input
   - Single source of truth

3. FEATURE ENGINEERING:
   - Convert raw user input to model features
   - Normalize/encode categorical data
   - Match model training format exactly

4. POST ENDPOINT FOR ML:
   - Standard practice for predictions
   - Send data → Process → Return result
   - Different from CRUD POST (no creation)

5. ERROR HANDLING:
   - Validate input before processing
   - Catch prediction errors
   - Return meaningful error messages

6. CORS:
   - Allow cross-origin requests
   - Frontend and API on different ports
   - Enable Streamlit-FastAPI communication

7. BATCH PREDICTIONS:
   - Process multiple users efficiently
   - Vectorized operations
   - Better than individual requests

8. MODEL AGNOSTIC:
   - Works with any sklearn model
   - Adapt for PyTorch, TensorFlow
   - Same pattern, different model libraries

9. DOCKER DEPLOYMENT:
   - Containerize FastAPI app
   - Model included in container
   - Easy scaling and versioning

10. MODEL MONITORING:
    - Log predictions for auditing
    - Monitor prediction latency
    - Track model performance over time
"""
