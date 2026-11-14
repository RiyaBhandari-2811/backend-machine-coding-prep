"""
schemas/prediction_response.py

Pydantic model for validating API output.
Improvement #8: Response model validation and documentation
"""

from pydantic import BaseModel, Field
from typing import Dict


class PredictionResponse(BaseModel):
    """
    Response model for prediction endpoint.
    
    Improvement #8: Uses Pydantic response_model to:
    1. Validate output before sending to client
    2. Auto-document in Swagger UI
    3. Provide examples and descriptions
    4. Filter unnecessary fields
    
    Example:
        {
            "predicted_category": "High",
            "confidence": 0.73,
            "class_probabilities": {
                "High": 0.73,
                "Medium": 0.17,
                "Low": 0.10
            }
        }
    """
    
    predicted_category: str = Field(
        ...,
        description="Predicted insurance premium category",
        example="High"
    )
    
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Model confidence for predicted category (0-1)",
        example=0.73
    )
    
    class_probabilities: Dict[str, float] = Field(
        ...,
        description="Probability score for each category",
        example={
            "High": 0.73,
            "Medium": 0.17,
            "Low": 0.10
        }
    )
