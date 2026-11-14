"""
schemas/user_input.py

Pydantic model for validating user input.
This module handles data validation and transformation.
Improvement #2: Field validation with @field_validator
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class UserInput(BaseModel):
    """
    User input validation model.
    
    Validates and preprocesses raw user data before prediction.
    
    Improvement #2: Uses @field_validator to normalize city names
    to title case automatically.
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
        description="Annual income in LPA",
        example=10
    )
    
    smoker: bool = Field(
        ...,
        description="Is user a smoker?",
        example=False
    )
    
    city: str = Field(
        ...,
        min_length=2,
        description="City of residence",
        example="Mumbai"
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
    
    # ======================================================================
    # FIELD VALIDATORS (Improvement #2)
    # ======================================================================
    
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v):
        """
        Normalize city name to title case.
        
        This validator ensures that city names are consistent:
        - "mumbai" → "Mumbai"
        - "  delhi  " → "Delhi"
        - "BANGALORE" → "Bangalore"
        
        This solves the problem where:
        - Before: "mumbai" (lowercase) didn't match "Mumbai" in tier-1 list
        - After: Automatically converted to "Mumbai"
        
        Returns:
            str: City name in title case
        """
        return v.strip().title()
