"""
Chapter 5: FastAPI - PUT & DELETE Endpoints (UPDATE & DELETE)
Complete CRUD: Create, Read, Update, Delete patient records.

Key concepts:
- HTTP PUT for updating existing resources
- HTTP DELETE for removing resources
- Optional fields for partial updates
- Recalculating computed fields (BMI, verdict)
- Path parameters to identify resource
- Status codes: 200 OK, 404 Not Found
- Complete CRUD operations
"""

import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Dict, Any, Optional

# ============================================================================
# SETUP
# ============================================================================

app = FastAPI(
    title="Patient Management API - Chapter 5",
    description="Complete CRUD: Create, Read, Update, Delete patients",
    version="5.0"
)

PATIENTS_FILE = "patients.json"


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class Patient(BaseModel):
    """
    Patient model for CREATE and response.
    All fields required.
    Includes computed fields (BMI, verdict).
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
        description="Patient full name"
    )
    city: str = Field(
        ...,
        min_length=1,
        description="City of residence"
    )
    age: int = Field(
        ...,
        gt=0,
        le=150,
        description="Age in years"
    )
    gender: Literal["Male", "Female", "Others"] = Field(
        ...,
        description="Patient gender"
    )
    height: float = Field(
        ...,
        gt=0,
        description="Height in meters"
    )
    weight: float = Field(
        ...,
        gt=0,
        description="Weight in kilograms"
    )
    
    @computed_field
    @property
    def bmi(self) -> float:
        """Automatically calculated BMI."""
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        """Automatically calculated BMI category."""
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"


class PatientUpdate(BaseModel):
    """
    Patient model for UPDATE - all fields optional.
    
    Use this for partial updates.
    Only include fields that need to change.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    city: Optional[str] = Field(None, min_length=1)
    age: Optional[int] = Field(None, gt=0, le=150)
    gender: Optional[Literal["Male", "Female", "Others"]] = None
    height: Optional[float] = Field(None, gt=0)
    weight: Optional[float] = Field(None, gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "city": "Mumbai",
                "weight": 90
            }
        }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def load_patients_data() -> Dict[str, Any]:
    """Load patient data from JSON file."""
    try:
        with open(PATIENTS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_patients_data(data: Dict[str, Any]) -> None:
    """Save patient data to JSON file."""
    with open(PATIENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
def root():
    """Root endpoint - API information."""
    return {
        "message": "Welcome to Patient Management API - Chapter 5",
        "chapter": "Complete CRUD: Update & Delete Endpoints",
        "operations": ["CREATE", "READ", "UPDATE", "DELETE"],
        "endpoints": 7
    }


# ============================================================================
# ENDPOINT 1: Retrieve all patients (GET)
# ============================================================================

@app.get("/patients")
def get_all_patients():
    """Retrieve all patient records."""
    data = load_patients_data()
    return {
        "total_patients": len(data),
        "patients": data
    }


# ============================================================================
# ENDPOINT 2: Retrieve specific patient (GET)
# ============================================================================

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    """Retrieve a specific patient by ID."""
    data = load_patients_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "patient_id": patient_id,
        "details": data[patient_id]
    }


# ============================================================================
# ENDPOINT 3: Sort and filter patients (GET with query params)
# ============================================================================

@app.get("/patients/search/sorted")
def get_sorted_patients(sort_by: str = "height", order: str = "asc"):
    """Retrieve patients sorted by specified field."""
    data = load_patients_data()
    
    valid_fields = ["height", "weight", "bmi", "age"]
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"sort_by must be one of: {valid_fields}"
        )
    
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="order must be 'asc' or 'desc'"
        )
    
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
# ENDPOINT 4: Create new patient (POST)
# ============================================================================

@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    """Create a new patient record."""
    data = load_patients_data()
    
    if patient.patient_id in data:
        raise HTTPException(
            status_code=400,
            detail=f"Patient {patient.patient_id} already exists"
        )
    
    patient_dict = patient.model_dump(exclude={"patient_id"})
    data[patient.patient_id] = patient_dict
    save_patients_data(data)
    
    return JSONResponse(
        status_code=201,
        content={
            "message": "Patient created successfully",
            "patient_id": patient.patient_id
        }
    )


# ============================================================================
# ENDPOINT 5: Update patient (PUT) - MAIN FOCUS OF CHAPTER 5
# ============================================================================

@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    """
    Update an existing patient record.
    
    Supports partial updates - only send fields to change.
    
    Args:
        patient_id: ID of patient to update (path parameter)
        patient_update: Fields to update (request body)
    
    Returns:
        200 OK - Patient updated successfully
        404 Not Found - Patient doesn't exist
    
    Example:
    PUT /patients/P001
    {
        "city": "Mumbai",
        "weight": 90
    }
    """
    
    # Step 1: Load all existing patients
    data = load_patients_data()
    
    # Step 2: Check if patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Step 3: Extract existing patient data
    existing_patient_info = data[patient_id]
    
    # Step 4: Convert update model to dict (only sent fields)
    # exclude_unset=True ensures only fields client sent are included
    update_dict = patient_update.model_dump(exclude_unset=True)
    
    # Step 5: Merge: Update existing with new values
    # Loop through each updated field and apply the change
    for key, value in update_dict.items():
        existing_patient_info[key] = value
    
    # Step 6: Recalculate computed fields (BMI, verdict)
    # Add patient_id back (required by Patient model)
    existing_patient_info["patient_id"] = patient_id
    
    # Create Pydantic object (triggers computed field calculation)
    patient_obj = Patient(**existing_patient_info)
    
    # Convert back to dict (with new BMI/verdict), exclude patient_id
    final_patient_data = patient_obj.model_dump(exclude={"patient_id"})
    
    # Step 7: Update database
    data[patient_id] = final_patient_data
    save_patients_data(data)
    
    # Step 8: Return success response
    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient updated successfully",
            "patient_id": patient_id,
            "updated_fields": list(update_dict.keys())
        }
    )


# ============================================================================
# ENDPOINT 6: Delete patient (DELETE) - ALSO NEW IN CHAPTER 5
# ============================================================================

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    """
    Delete a patient record.
    
    Args:
        patient_id: ID of patient to delete (path parameter)
    
    Returns:
        200 OK - Patient deleted successfully
        404 Not Found - Patient doesn't exist
    
    Example:
    DELETE /patients/P001
    """
    
    # Step 1: Load all existing patients
    data = load_patients_data()
    
    # Step 2: Check if patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Step 3: Delete the patient
    del data[patient_id]
    
    # Step 4: Save to database
    save_patients_data(data)
    
    # Step 5: Return success response
    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient deleted successfully",
            "deleted_patient_id": patient_id
        }
    )


# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================

"""
How to test this API:

1. START THE SERVER:
   uvicorn main:app --reload

2. OPEN SWAGGER UI:
   http://localhost:8000/docs

TEST PUT (UPDATE) ENDPOINT:
==============================

Partial Update (Recommended):
PUT /patients/P001
{
    "city": "Mumbai",
    "weight": 90
}
Expected: 200 OK, BMI and verdict recalculated

Full Update:
PUT /patients/P002
{
    "name": "Jane Doe",
    "city": "Delhi",
    "age": 30,
    "gender": "Female",
    "height": 1.65,
    "weight": 65
}
Expected: 200 OK, all fields updated

Error Cases:
PUT /patients/P999 (non-existent)
Expected: 404 Not Found

PUT /patients/P001
{"age": -5}
Expected: Validation error (age must be > 0)


TEST DELETE ENDPOINT:
==============================

Normal Delete:
DELETE /patients/P006
Expected: 200 OK, Patient deleted

Verify Delete:
GET /patients
Expected: P006 is no longer in list

Delete Non-existent:
DELETE /patients/P999
Expected: 404 Not Found

Delete Already Deleted:
DELETE /patients/P006 (second time)
Expected: 404 Not Found


VERIFY UPDATES:
==============================

After updating weight:
GET /patients/P001
Expected: Weight changed, BMI recalculated, verdict updated

Example: If weight 95 → 90, BMI might change from 29.39 to 27.76
Example: Verdict might change from "Overweight" to "Normal"
"""


# ============================================================================
# KEY CONCEPTS SUMMARY
# ============================================================================

"""
CHAPTER 5 KEY LEARNINGS:

1. HTTP METHODS:
   - PUT: Update existing resource (idempotent)
   - DELETE: Remove resource (not idempotent - second call fails)

2. PARTIAL UPDATES:
   - Use Optional fields in request body model
   - Only send fields that need changing
   - Client can update 1 field or all fields

3. EXCLUDE_UNSET PATTERN:
   - Prevents None from overwriting data
   - Only includes fields client actually sent
   - Crucial for partial updates

4. RECALCULATING COMPUTED FIELDS:
   - Convert Pydantic → dict → Pydantic → dict
   - Ensures BMI/verdict match new weight/height
   - Done automatically via computed_field decorator

5. PATH PARAMETERS:
   - Identify which resource to update/delete
   - Example: /patients/{patient_id}
   - Must validate existence (404 if not found)

6. STATUS CODES:
   - 200 OK: Update or delete successful
   - 404 Not Found: Resource doesn't exist
   - No 201 for PUT (201 is only for POST)

7. COMPLETE CRUD:
   CREATE: POST /create
   READ:   GET /patients, GET /patients/{id}, GET /patients/search/sorted
   UPDATE: PUT /patients/{id}
   DELETE: DELETE /patients/{id}

8. IDEMPOTENCY:
   - PUT: idempotent (same result each time)
   - DELETE: not idempotent (fails on second call)

9. MERGE LOGIC:
   - Load existing data
   - Update changed fields only
   - Preserve unchanged fields
   - Recalculate dependent fields

10. ERROR HANDLING:
    - Always check if resource exists first
    - Validate incoming data with Pydantic
    - Return appropriate status codes and error messages
"""
