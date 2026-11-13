"""
Chapter 4: FastAPI - POST Endpoint (CREATE)
Create new patient records with Pydantic validation and computed fields.

Key concepts:
- HTTP POST requests for creating resources
- Request body with JSON data
- Pydantic models for validation
- Computed fields (BMI, verdict auto-calculation)
- HTTP status codes: 201 (Created), 400 (Bad Request)
- Duplicate prevention
"""

import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Dict, Any

# ============================================================================
# SETUP
# ============================================================================

app = FastAPI(
    title="Patient Management API - Chapter 4",
    description="POST endpoint for creating new patient records",
    version="4.0"
)

# Path to patient data file
PATIENTS_FILE = "patients.json"


# ============================================================================
# PYDANTIC MODEL WITH VALIDATION
# ============================================================================

class Patient(BaseModel):
    """
    Patient model with validation rules and computed fields.
    
    Validates:
    - All fields required
    - Age: 0 < age ≤ 150
    - Height, Weight: Must be positive
    - Gender: Only Male, Female, Others
    
    Computes:
    - BMI: weight / (height²)
    - Verdict: Based on BMI category
    """
    
    patient_id: str = Field(
        ...,
        description="Unique patient identifier",
        examples=["P001", "P006"]
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Patient full name",
        examples=["Rahul Gupta"]
    )
    city: str = Field(
        ...,
        min_length=1,
        description="City of residence",
        examples=["Hyderabad", "Mumbai"]
    )
    age: int = Field(
        ...,
        gt=0,
        le=150,
        description="Patient age in years",
        examples=[25, 45, 65]
    )
    gender: Literal["Male", "Female", "Others"] = Field(
        ...,
        description="Patient gender",
        examples=["Male", "Female"]
    )
    height: float = Field(
        ...,
        gt=0,
        description="Patient height in meters",
        examples=[1.75, 1.60, 1.80]
    )
    weight: float = Field(
        ...,
        gt=0,
        description="Patient weight in kilograms",
        examples=[70, 65, 80]
    )
    
    @computed_field
    @property
    def bmi(self) -> float:
        """
        Automatically calculated BMI.
        Formula: weight / (height²)
        """
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        """
        Automatically calculated BMI category.
        Based on WHO standards.
        """
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def load_patients_data() -> Dict[str, Any]:
    """
    Load patient data from JSON file.
    
    Returns:
        Dictionary with patient_id as key, patient data as value
        Returns empty dict if file doesn't exist
    """
    try:
        with open(PATIENTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_patients_data(data: Dict[str, Any]) -> None:
    """
    Save patient data to JSON file.
    
    Args:
        data: Dictionary to save to file
    """
    with open(PATIENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ============================================================================
# ROOT ENDPOINT (Information)
# ============================================================================

@app.get("/")
def root():
    """Root endpoint - API information."""
    return {
        "message": "Welcome to Patient Management API - Chapter 4",
        "chapter": "POST Endpoint for Creating Patients",
        "concepts": [
            "HTTP POST requests",
            "Request body with JSON data",
            "Pydantic validation",
            "Computed fields (BMI, verdict)",
            "HTTP status codes (201, 400)"
        ]
    }


# ============================================================================
# ENDPOINT 1: Retrieve all patients (GET)
# ============================================================================

@app.get("/patients")
def get_all_patients():
    """
    Retrieve all patient records.
    
    Returns:
        Dictionary with all patients
        Status: 200 OK
    """
    data = load_patients_data()
    return {
        "total_patients": len(data),
        "patients": data
    }


# ============================================================================
# ENDPOINT 2: Create new patient (POST) - MAIN FOCUS
# ============================================================================

@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    """
    Create a new patient record.
    
    Steps:
    1. Pydantic validates request body
    2. Check for duplicate patient_id
    3. Add to database
    4. Save to file
    5. Return 201 response
    
    Args:
        patient: Patient data from request body (validated by Pydantic)
    
    Returns:
        201 Created - Patient created successfully
        400 Bad Request - Patient already exists
    
    Raises:
        HTTPException: If patient_id already exists
    
    Example request body:
    {
        "patient_id": "P006",
        "name": "Rahul Gupta",
        "city": "Hyderabad",
        "age": 19,
        "gender": "Male",
        "height": 1.74,
        "weight": 55
    }
    
    Example response (201):
    {
        "message": "Patient created successfully",
        "patient_id": "P006"
    }
    """
    
    # Step 1: Load existing patient data
    data = load_patients_data()
    
    # Step 2: Check if patient already exists
    if patient.patient_id in data:
        raise HTTPException(
            status_code=400,
            detail=f"Patient {patient.patient_id} already exists"
        )
    
    # Step 3: Convert Pydantic model to dictionary
    # Exclude patient_id because we'll use it as the dictionary key
    patient_dict = patient.model_dump(exclude={"patient_id"})
    # Note: Computed fields (bmi, verdict) are automatically included!
    
    # Step 4: Add new patient to database
    data[patient.patient_id] = patient_dict
    
    # Step 5: Save to file
    save_patients_data(data)
    
    # Step 6: Return success response
    return JSONResponse(
        status_code=201,
        content={
            "message": "Patient created successfully",
            "patient_id": patient.patient_id,
            "status": "Created"
        }
    )


# ============================================================================
# ENDPOINT 3: Retrieve specific patient (GET)
# ============================================================================

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    """
    Retrieve a specific patient by ID.
    
    Args:
        patient_id: Patient ID to retrieve
    
    Returns:
        Patient data if found
        404 Not Found - If patient doesn't exist
    """
    data = load_patients_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "patient_id": patient_id,
        "details": data[patient_id]
    }


# ============================================================================
# ENDPOINT 4: Sort and filter patients (GET with query parameters)
# ============================================================================

@app.get("/patients/search/sorted")
def get_sorted_patients(
    sort_by: str = "height",
    order: str = "asc"
):
    """
    Retrieve patients sorted by specified field.
    
    Args:
        sort_by: Field to sort by (height, weight, bmi, age)
        order: Sort order (asc=ascending, desc=descending)
    
    Returns:
        Sorted list of patients
        400 Bad Request - Invalid sort_by or order
    """
    data = load_patients_data()
    
    # Validate sort_by parameter
    valid_fields = ["height", "weight", "bmi", "age"]
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"sort_by must be one of: {valid_fields}"
        )
    
    # Validate order parameter
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="order must be 'asc' or 'desc'"
        )
    
    # Sort patients
    sorted_patients = sorted(
        data.items(),
        key=lambda x: x[1][sort_by],
        reverse=(order == "desc")
    )
    
    return {
        "sort_by": sort_by,
        "order": order,
        "total_patients": len(sorted_patients),
        "patients": {pid: pdata for pid, pdata in sorted_patients}
    }


# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================

"""
How to test this API:

1. START THE SERVER:
   uvicorn main:app --reload

2. OPEN SWAGGER UI:
   http://localhost:8000/docs

3. TEST THE POST ENDPOINT:
   - Click on POST /create
   - Click "Try it out"
   - Fill in the request body:
   
   {
       "patient_id": "P007",
       "name": "John Doe",
       "city": "Mumbai",
       "age": 30,
       "gender": "Male",
       "height": 1.78,
       "weight": 75
   }
   
   - Click "Execute"
   - Expected response: 201 Created

4. ERRORS TO TEST:
   
   a) Duplicate patient_id:
      - Try creating with P007 again
      - Expected: 400 Bad Request - Patient already exists
   
   b) Invalid age (out of range):
      {
          "patient_id": "P008",
          "name": "Jane",
          "city": "Delhi",
          "age": -5,
          "gender": "Female",
          "height": 1.65,
          "weight": 60
      }
      Expected: Validation error (age must be > 0)
   
   c) Invalid gender:
      Replace "Female" with "Unknown"
      Expected: Validation error (invalid literal)
   
   d) Missing required field:
      Remove the "age" field
      Expected: Validation error (field required)

5. VERIFY COMPUTED FIELDS:
   - After creating a patient, check the response
   - BMI and verdict should be automatically calculated
   - Example: For height=1.74, weight=55:
     - BMI = 55 / (1.74²) = 18.18 (Underweight)
     - Verdict = "Underweight"

6. CHECK ALL PATIENTS:
   - GET /patients → See all patients including newly created ones
   - GET /patients/{id} → See specific patient
   - GET /patients/search/sorted?sort_by=bmi&order=desc → See sorted patients
"""


# ============================================================================
# MAIN CONCEPTS SUMMARY
# ============================================================================

"""
KEY LEARNINGS FROM CHAPTER 4:

1. HTTP METHODS:
   - GET: Retrieve data (idempotent, no body)
   - POST: Create data (not idempotent, with body)

2. REQUEST BODY:
   - Sent by client in POST/PUT/PATCH requests
   - Usually JSON format
   - Can contain complex nested data

3. PYDANTIC MODELS:
   - Validates request body automatically
   - Type checking and constraint validation
   - Provides auto-generated documentation
   - Includes computed fields automatically in response

4. COMPUTED FIELDS:
   - Calculated from other fields using @computed_field
   - Not sent by client, calculated by server
   - Ensures single source of truth
   - Automatically included in model_dump()

5. VALIDATION FLOW:
   Request → Pydantic Model → Validation → If valid → Process
                                         → If invalid → 400 error

6. STATUS CODES:
   - 201 Created: Resource successfully created
   - 400 Bad Request: Invalid data or duplicate
   - 404 Not Found: Resource doesn't exist

7. DUPLICATE PREVENTION:
   - Check if resource exists before creating
   - Return 400 if duplicate found
   - Prevents data inconsistency
"""
