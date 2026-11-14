"""
FastAPI Patient Management System - Chapter 2
Demonstrates HTTP Methods and CRUD Operations
"""

from fastapi import FastAPI
from typing import List, Dict, Any
import json
import os

app = FastAPI(
    title="Patient Management System API",
    description="API to manage patient records with CRUD operations",
    version="1.0.0"
)

# ============================================================================
# FILE PATHS AND CONSTANTS
# ============================================================================

# Path to patients.json file
PATIENTS_FILE = os.path.join(os.path.dirname(__file__), "patients.json")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_patients_data() -> List[Dict[str, Any]]:
    """
    Load patient data from JSON file.
    
    Returns:
        List of patient dictionaries
    """
    try:
        with open(PATIENTS_FILE, 'r') as f:
            patients = json.load(f)
        return patients
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_patients_data(patients: List[Dict[str, Any]]) -> None:
    """
    Save patient data to JSON file.
    
    Args:
        patients: List of patient dictionaries to save
    """
    with open(PATIENTS_FILE, 'w') as f:
        json.dump(patients, f, indent=2)


# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get("/")
async def read_root():
    """
    Root endpoint - Welcome message
    HTTP Method: GET (Retrieve)
    """
    return {
        "message": "Patient Management System API",
        "description": "A fully functional API to manage your patients' records"
    }


@app.get("/about")
async def about():
    """
    About endpoint - API information
    HTTP Method: GET (Retrieve)
    """
    return {
        "app": "Patient Management System",
        "version": "1.0.0",
        "description": "API to manage patient records with full CRUD operations",
        "features": [
            "Create new patient records",
            "View all patients",
            "View specific patient",
            "Update patient information",
            "Delete patient records"
        ]
    }


# ============================================================================
# PATIENT ENDPOINTS - CRUD OPERATIONS
# ============================================================================

@app.get("/patients", tags=["Patients - Retrieve"])
async def get_all_patients():
    """
    Get all patients
    
    HTTP Method: GET (Retrieve/Read)
    CRUD Operation: READ
    
    Returns:
        List of all patients in the system
    
    Example Response:
        [
            {
                "id": 1,
                "name": "Rajesh Kumar",
                "age": 35,
                "height": 180,
                "weight": 75,
                "bmi": 23.15
            },
            ...
        ]
    """
    patients = load_patients_data()
    return {
        "total": len(patients),
        "patients": patients
    }


@app.get("/patients/{patient_id}", tags=["Patients - Retrieve"])
async def get_patient_by_id(patient_id: int):
    """
    Get a specific patient by ID
    
    HTTP Method: GET (Retrieve/Read)
    CRUD Operation: READ
    
    Args:
        patient_id: The ID of the patient to retrieve
    
    Returns:
        Patient object if found, error message if not found
    
    Example Response:
        {
            "id": 1,
            "name": "Rajesh Kumar",
            "age": 35,
            "height": 180,
            "weight": 75,
            "bmi": 23.15
        }
    """
    patients = load_patients_data()
    
    for patient in patients:
        if patient["id"] == patient_id:
            return patient
    
    return {
        "error": f"Patient with ID {patient_id} not found",
        "status": 404
    }


@app.post("/patients", tags=["Patients - Create"])
async def create_patient(name: str, age: int, height: int, weight: float):
    """
    Create a new patient record
    
    HTTP Method: POST (Create)
    CRUD Operation: CREATE
    
    Args:
        name: Patient's full name
        age: Patient's age in years
        height: Patient's height in cm
        weight: Patient's weight in kg
    
    Returns:
        Created patient object with auto-generated ID
    
    Example Request:
        POST /patients?name=John Doe&age=30&height=180&weight=70
    
    Example Response:
        {
            "id": 6,
            "name": "John Doe",
            "age": 30,
            "height": 180,
            "weight": 70,
            "bmi": 21.6
        }
    """
    patients = load_patients_data()
    
    # Calculate BMI
    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 2)
    
    # Generate new ID
    new_id = max([p["id"] for p in patients], default=0) + 1
    
    # Create new patient
    new_patient = {
        "id": new_id,
        "name": name,
        "age": age,
        "height": height,
        "weight": weight,
        "bmi": bmi
    }
    
    # Add to list and save
    patients.append(new_patient)
    save_patients_data(patients)
    
    return {
        "message": "Patient created successfully",
        "patient": new_patient
    }


@app.patch("/patients/{patient_id}", tags=["Patients - Update"])
async def update_patient_partial(
    patient_id: int,
    name: str = None,
    age: int = None,
    height: int = None,
    weight: float = None
):
    """
    Partially update a patient record (PATCH)
    
    HTTP Method: PATCH (Update - Partial)
    CRUD Operation: UPDATE
    
    Args:
        patient_id: The ID of the patient to update
        name: Patient's name (optional)
        age: Patient's age (optional)
        height: Patient's height (optional)
        weight: Patient's weight (optional)
    
    Returns:
        Updated patient object
    
    Example Request:
        PATCH /patients/1?weight=72
    
    Note:
        Only updates the fields you provide. Other fields remain unchanged.
        If weight is updated, BMI is automatically recalculated.
    """
    patients = load_patients_data()
    
    for i, patient in enumerate(patients):
        if patient["id"] == patient_id:
            # Update only provided fields
            if name is not None:
                patient["name"] = name
            if age is not None:
                patient["age"] = age
            if height is not None:
                patient["height"] = height
            if weight is not None:
                patient["weight"] = weight
            
            # Recalculate BMI if height or weight changed
            height_m = patient["height"] / 100
            patient["bmi"] = round(patient["weight"] / (height_m ** 2), 2)
            
            # Save and return
            save_patients_data(patients)
            return {
                "message": "Patient updated successfully",
                "patient": patient
            }
    
    return {
        "error": f"Patient with ID {patient_id} not found",
        "status": 404
    }


@app.put("/patients/{patient_id}", tags=["Patients - Update"])
async def update_patient_full(
    patient_id: int,
    name: str,
    age: int,
    height: int,
    weight: float
):
    """
    Fully replace a patient record (PUT)
    
    HTTP Method: PUT (Update - Full Replacement)
    CRUD Operation: UPDATE
    
    Args:
        patient_id: The ID of the patient to replace
        name: Patient's name (required)
        age: Patient's age (required)
        height: Patient's height (required)
        weight: Patient's weight (required)
    
    Returns:
        Updated patient object
    
    Example Request:
        PUT /patients/1?name=John Smith&age=31&height=180&weight=72
    
    Note:
        All fields are required. This replaces the entire record.
        Use PATCH if you only want to update specific fields.
    """
    patients = load_patients_data()
    
    for i, patient in enumerate(patients):
        if patient["id"] == patient_id:
            # Calculate new BMI
            height_m = height / 100
            bmi = round(weight / (height_m ** 2), 2)
            
            # Replace entire patient record
            patients[i] = {
                "id": patient_id,
                "name": name,
                "age": age,
                "height": height,
                "weight": weight,
                "bmi": bmi
            }
            
            # Save and return
            save_patients_data(patients)
            return {
                "message": "Patient record replaced successfully",
                "patient": patients[i]
            }
    
    return {
        "error": f"Patient with ID {patient_id} not found",
        "status": 404
    }


@app.delete("/patients/{patient_id}", tags=["Patients - Delete"])
async def delete_patient(patient_id: int):
    """
    Delete a patient record
    
    HTTP Method: DELETE (Delete)
    CRUD Operation: DELETE
    
    Args:
        patient_id: The ID of the patient to delete
    
    Returns:
        Confirmation message with deleted patient details
    
    Example Request:
        DELETE /patients/1
    
    Example Response:
        {
            "message": "Patient deleted successfully",
            "deleted_patient": {
                "id": 1,
                "name": "Rajesh Kumar",
                ...
            }
        }
    """
    patients = load_patients_data()
    
    for i, patient in enumerate(patients):
        if patient["id"] == patient_id:
            deleted = patients.pop(i)
            save_patients_data(patients)
            return {
                "message": "Patient deleted successfully",
                "deleted_patient": deleted
            }
    
    return {
        "error": f"Patient with ID {patient_id} not found",
        "status": 404
    }


# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.get("/stats", tags=["Statistics"])
async def get_stats():
    """
    Get statistics about patients in the system
    
    HTTP Method: GET
    """
    patients = load_patients_data()
    
    if not patients:
        return {
            "total_patients": 0,
            "message": "No patients in system"
        }
    
    ages = [p["age"] for p in patients]
    weights = [p["weight"] for p in patients]
    bmis = [p["bmi"] for p in patients]
    
    return {
        "total_patients": len(patients),
        "average_age": round(sum(ages) / len(ages), 2),
        "average_weight": round(sum(weights) / len(weights), 2),
        "average_bmi": round(sum(bmis) / len(bmis), 2),
        "age_range": {
            "min": min(ages),
            "max": max(ages)
        },
        "weight_range": {
            "min": min(weights),
            "max": max(weights)
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
