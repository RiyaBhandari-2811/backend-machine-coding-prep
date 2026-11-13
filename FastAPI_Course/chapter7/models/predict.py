"""
models/predict.py

Machine Learning model loading and prediction logic.
Improvement #5: Separation of concerns - ML logic in separate file
"""

import pickle
import pandas as pd
from pathlib import Path
from config.city_tier import TIER_1_CITIES, TIER_2_CITIES

# Model version
MODEL_VERSION = "1.0.0"


def load_model():
    """
    Load pre-trained ML model from pickle file.
    
    Returns:
        sklearn model: Trained Random Forest classifier
    
    Raises:
        FileNotFoundError: If model.pkl not found
    """
    model_path = Path(__file__).parent / "model.pkl"
    
    with open(model_path, 'rb') as f:
        return pickle.load(f)


def compute_bmi(weight: float, height: float) -> float:
    """Calculate BMI from weight and height."""
    return round(weight / (height ** 2), 2)


def compute_age_group(age: int) -> str:
    """Categorize age into groups."""
    if age < 25:
        return "Young"
    elif age < 45:
        return "Adult"
    elif age < 60:
        return "Middle-aged"
    else:
        return "Senior"


def compute_lifestyle_risk(bmi: float, smoker: bool) -> str:
    """Compute lifestyle risk from BMI and smoker status."""
    if smoker and bmi > 30:
        return "High"
    elif smoker and bmi > 27:
        return "Medium"
    elif bmi > 30:
        return "Medium"
    else:
        return "Low"


def compute_city_tier(city: str) -> int:
    """Compute city tier from city name."""
    if city in TIER_1_CITIES:
        return 1
    elif city in TIER_2_CITIES:
        return 2
    else:
        return 3


def predict_output(user_input: dict) -> dict:
    """
    Make prediction using ML model.
    
    Improvement #6: Returns confidence scores and probabilities
    Improvement #7: Error handling with try-catch
    
    Args:
        user_input: Dictionary with user data {
            age, weight, height, income_lpa, smoker, city, occupation
        }
    
    Returns:
        dict: {
            predicted_category: str (High/Medium/Low),
            confidence: float (0-1),
            class_probabilities: dict
        }
    
    Raises:
        Exception: Any error in prediction
    """
    try:
        # Load model
        model = load_model()
        
        # Compute features
        bmi = compute_bmi(user_input['weight'], user_input['height'])
        age_group = compute_age_group(user_input['age'])
        lifestyle_risk = compute_lifestyle_risk(bmi, user_input['smoker'])
        city_tier = compute_city_tier(user_input['city'])
        
        # Build feature dictionary
        features = {
            'bmi': bmi,
            'age_group': age_group,
            'lifestyle_risk': lifestyle_risk,
            'city_tier': city_tier,
            'income_lpa': user_input['income_lpa'],
            'occupation': user_input['occupation']
        }
        
        # Create DataFrame for model
        input_df = pd.DataFrame([features])
        
        # Get prediction
        prediction = model.predict(input_df)[0]
        
        # Get prediction probabilities (Improvement #6)
        probabilities = model.predict_proba(input_df)[0]
        class_names = model.classes_
        
        # Build probability dictionary
        prob_dict = {
            name: float(prob)
            for name, prob in zip(class_names, probabilities)
        }
        
        # Return result
        return {
            "predicted_category": prediction,
            "confidence": float(prob_dict[prediction]),
            "class_probabilities": prob_dict
        }
    
    except Exception as e:
        # Improvement #7: Error handling
        raise Exception(f"Prediction error: {str(e)}")
