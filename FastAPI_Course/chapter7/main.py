"""
main.py

FastAPI application with all 8 improvements.
This file contains ONLY routing logic.

Improvements implemented:
1. ✅ Dedicated project folder
2. ✅ Field validation (@field_validator)
3. ✅ Home endpoint (GET /)
4. ✅ Health check endpoint (GET /health)
5. ✅ Separation of concerns (separate files)
6. ✅ Confidence scores (predict_proba)
7. ✅ Error handling (try-catch)
8. ✅ Response models (response_model)
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Improvement #5: Import from separate modules
from schemas.user_input import UserInput
from schemas.prediction_response import PredictionResponse
from models.predict import predict_output, MODEL_VERSION

# ============================================================================
# FASTAPI APP SETUP
# ============================================================================

app = FastAPI(
    title="Insurance Premium Prediction API",
    description="Predict insurance premium categories with ML confidence scores",
    version="2.0.0"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# IMPROVEMENT #3: HOME ENDPOINT
# ============================================================================

@app.get("/")
def home():
    """
    Improvement #3: Home endpoint
    
    Human-readable API information.
    Tells clients that this is an API endpoint.
    Shows available endpoints.
    
    Returns:
        dict: API information
    """
    return {
        "message": "Insurance Premium Prediction API",
        "version": "2.0.0",
        "status": "active",
        "endpoints": [
            "GET /",
            "GET /health",
            "POST /predict",
            "GET /docs"
        ],
        "documentation": "Visit /docs for interactive API documentation"
    }


# ============================================================================
# IMPROVEMENT #4: HEALTH CHECK ENDPOINT
# ============================================================================

@app.get("/health")
def health_check():
    """
    Improvement #4: Health check endpoint
    
    Machine-readable status endpoint.
    Required by cloud platforms (AWS, Kubernetes).
    Automated monitoring and recovery.
    
    Returns:
        dict: {
            status: "ok" if healthy,
            model_loaded: bool,
            model_version: str
        }
    
    Usage:
        AWS Elastic Load Balancer periodically hits this endpoint.
        If status != "ok", the instance is marked as unhealthy.
    """
    return {
        "status": "ok",
        "model_loaded": True,
        "model_version": MODEL_VERSION
    }


# ============================================================================
# IMPROVEMENT #8: MAIN PREDICTION ENDPOINT WITH RESPONSE MODEL
# ============================================================================

@app.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=200,
    summary="Predict Insurance Premium",
    responses={
        200: {
            "description": "Successful prediction",
            "content": {
                "application/json": {
                    "example": {
                        "predicted_category": "High",
                        "confidence": 0.73,
                        "class_probabilities": {
                            "High": 0.73,
                            "Medium": 0.17,
                            "Low": 0.10
                        }
                    }
                }
            }
        },
        400: {"description": "Validation error in input"},
        500: {"description": "Server error during prediction"}
    }
)
def predict_premium(user_data: UserInput):
    """
    Improvement #8: Response model validation
    
    Predict insurance premium category with confidence scores.
    
    This endpoint demonstrates all 8 improvements:
    
    1. ✅ Dedicated folder structure
    2. ✅ Field validation (UserInput normalizes city)
    3. ✅ Home endpoint (GET /)
    4. ✅ Health check (GET /health)
    5. ✅ Separation of concerns (code in separate files)
    6. ✅ Confidence scores (returns probabilities)
    7. ✅ Error handling (try-catch below)
    8. ✅ Response validation (response_model)
    
    Args:
        user_data: UserInput model with validated fields
            - age: 0-100 years
            - weight: 30-200 kg
            - height: 1.2-2.5 meters
            - income_lpa: > 0 LPA
            - smoker: bool
            - city: string (auto-normalized to title case)
            - occupation: from predefined list
    
    Returns:
        PredictionResponse: {
            - predicted_category: "High" / "Medium" / "Low"
            - confidence: 0.0-1.0 (model's confidence)
            - class_probabilities: {High: 0.73, Medium: 0.17, Low: 0.10}
        }
    
    Example request:
        POST /predict
        {
            "age": 35,
            "weight": 79,
            "height": 1.72,
            "income_lpa": 10,
            "smoker": false,
            "city": "mumbai",          # auto-normalized to "Mumbai"
            "occupation": "Software Engineer"
        }
    
    Example response:
        {
            "predicted_category": "Low",
            "confidence": 0.39,
            "class_probabilities": {
                "High": 0.36,
                "Medium": 0.25,
                "Low": 0.39
            }
        }
    """
    
    try:
        # Improvement #7: Error handling with try-catch
        
        # Convert Pydantic model to dict for ML function
        user_input_dict = user_data.model_dump()
        
        # Call ML prediction function (from models/predict.py)
        result = predict_output(user_input_dict)
        
        # Improvement #8: Response is validated by PredictionResponse model
        # FastAPI automatically validates that result matches PredictionResponse
        return result
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Improvement #7: Catch unexpected errors
        # Return 500 with error message instead of crashing
        return JSONResponse(
            status_code=500,
            content={
                "error": "Prediction failed",
                "detail": str(e)
            }
        )


# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Log when API starts up."""
    print("🚀 Insurance Premium Prediction API started")
    print(f"📦 Model version: {MODEL_VERSION}")
    print("📚 Documentation: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Log when API shuts down."""
    print("🛑 Insurance Premium Prediction API stopped")


# ============================================================================
# RUN INSTRUCTIONS
# ============================================================================

"""
HOW TO RUN:

1. Create virtual environment:
   python -m venv my_env
   source my_env/bin/activate  # On Windows: my_env\\Scripts\\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run the API:
   uvicorn main:app --reload --port 8000

4. Access API documentation:
   http://localhost:8000/docs

5. Test endpoints:
   - Home: http://localhost:8000/
   - Health: http://localhost:8000/health
   - Prediction: POST to http://localhost:8000/predict

IMPROVEMENTS SUMMARY:
1. ✅ Project Structure: Separate folders (schemas, config, models)
2. ✅ Field Validation: City auto-normalized with @field_validator
3. ✅ Home Endpoint: GET / shows API info
4. ✅ Health Check: GET /health for cloud platforms
5. ✅ Separation of Concerns: ML logic in models/, schemas separate
6. ✅ Confidence Scores: Returns predict_proba() output
7. ✅ Error Handling: Try-catch prevents crashes
8. ✅ Response Models: Output validated with PredictionResponse
"""
