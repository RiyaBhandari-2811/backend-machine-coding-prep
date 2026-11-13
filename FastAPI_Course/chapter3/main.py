"""
FastAPI Chapter 3: Path Parameters, Query Parameters & HTTP Status Codes

This module demonstrates:
1. Path parameters with validation using Path()
2. Query parameters for sorting and filtering
3. HTTP status codes in practice
4. HTTPException for proper error handling
5. Combining path and query parameters effectively

Key Endpoints:
- GET /patients - List all patients with optional sorting
- GET /patients/{patient_id} - Get specific patient
- GET /patients/sort - Sort patients by various fields
- POST /patients - Create new patient
- PATCH /patients/{patient_id} - Update patient
- DELETE /patients/{patient_id} - Delete patient
"""

import json
from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional, List
from datetime import datetime

app = FastAPI(
    title="Patient Management API - Chapter 3",
    description="Comprehensive API with Path & Query Parameters, Status Codes, and Error Handling",
    version="3.0"
)

# ============================================================================
# UTILITY FUNCTIONS FOR DATA MANAGEMENT
# ============================================================================

def load_patients_data():
    """
    Load all patients from JSON file.
    
    Returns:
        dict: Dictionary with patient_id as key and patient data as value
    
    Raises:
        HTTPException: If file not found
    """
    try:
        with open("chapter3/patients.json", "r") as file:
            data = json.load(file)
            # Convert list to dictionary with ID as key
            return {patient["id"]: patient for patient in data}
    except FileNotFoundError:
        # Load from chapter2 if chapter3 doesn't exist yet
        try:
            with open("chapter2/patients.json", "r") as file:
                data = json.load(file)
                return {patient["id"]: patient for patient in data}
        except FileNotFoundError:
            raise HTTPException(
                status_code=500,
                detail="Patient database not found"
            )


def save_patients_data(patients_dict):
    """
    Save patients to JSON file.
    
    Args:
        patients_dict (dict): Dictionary of patients to save
    """
    data = list(patients_dict.values())
    with open("chapter3/patients.json", "w") as file:
        json.dump(data, file, indent=2)


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculate BMI from weight and height.
    
    Formula: BMI = weight (kg) / height² (m²)
    
    Args:
        weight_kg (float): Weight in kilograms
        height_m (float): Height in meters
    
    Returns:
        float: Calculated BMI rounded to 2 decimal places
    """
    if height_m == 0:
        return 0
    return round(weight_kg / (height_m ** 2), 2)


# ============================================================================
# BASIC ENDPOINTS
# ============================================================================

@app.get("/", tags=["Health Check"])
async def root():
    """
    Root endpoint - API welcome message.
    
    Returns:
        dict: Welcome message and API info
    """
    return {
        "message": "Welcome to Patient Management API - Chapter 3",
        "version": "3.0",
        "features": [
            "Path Parameters with Validation",
            "Query Parameters for Sorting/Filtering",
            "HTTP Status Codes",
            "Error Handling with HTTPException"
        ]
    }


@app.get("/about", tags=["Information"])
async def about():
    """
    About endpoint - API documentation and features.
    
    Returns:
        dict: API description with features
    """
    return {
        "name": "Patient Management API",
        "chapter": 3,
        "features": {
            "path_parameters": "Retrieve specific patients by ID with validation",
            "query_parameters": "Sort and filter patient data",
            "status_codes": "Proper HTTP status codes for all operations",
            "error_handling": "HTTPException for graceful error responses"
        },
        "endpoints_count": 6
    }


# ============================================================================
# PATH PARAMETERS ENDPOINTS
# ============================================================================

@app.get("/patients", tags=["Patients"])
async def list_patients():
    """
    Get all patients.
    
    HTTP Status Codes:
    - 200: Successfully retrieved all patients
    
    Returns:
        dict: List of all patients with count
    """
    patients = load_patients_data()
    return {
        "total": len(patients),
        "patients": list(patients.values())
    }


@app.get("/patients/{patient_id}", tags=["Patients"])
async def get_patient(
    patient_id: str = Path(
        ...,
        title="Patient ID",
        description="The unique identifier of the patient in the database",
        example="P001",
        min_length=1,
        max_length=10
    )
):
    """
    Get a specific patient by ID.
    
    This endpoint demonstrates:
    - Path parameter extraction from URL
    - Path parameter validation
    - 404 error handling when patient not found
    
    Args:
        patient_id (str): The ID of the patient to retrieve
    
    HTTP Status Codes:
    - 200: Patient found and returned
    - 404: Patient not found in database
    
    Returns:
        dict: Patient information with all details
    
    Raises:
        HTTPException: If patient with given ID doesn't exist
    
    Example:
        GET /patients/P001 → Returns patient P001 data
    """
    patients = load_patients_data()
    
    # Check if patient exists
    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with ID '{patient_id}' not found in database"
        )
    
    return {
        "status": "success",
        "patient": patients[patient_id]
    }


# ============================================================================
# QUERY PARAMETERS ENDPOINTS - SORTING & FILTERING
# ============================================================================

@app.get("/patients/search/sorted", tags=["Patients", "Sorting"])
async def get_sorted_patients(
    sort_by: str = Query(
        "id",
        title="Sort Field",
        description="Field to sort patients by",
        example="weight"
    ),
    order: str = Query(
        "ascending",
        title="Sort Order",
        description="Order to sort in: ascending or descending",
        example="ascending"
    )
):
    """
    Get patients sorted by specified field and order.
    
    This endpoint demonstrates:
    - Query parameter declaration with Query()
    - Input validation for query parameters
    - Dynamic sorting based on user input
    - Error handling for invalid sort fields
    
    Args:
        sort_by (str): Field to sort by (weight, height, bmi, age)
        order (str): Sort order (ascending, descending)
    
    HTTP Status Codes:
    - 200: Sorting successful
    - 400: Invalid sort_by or order parameter
    
    Query Parameters:
    - sort_by: weight, height, bmi, age (default: id)
    - order: ascending, descending (default: ascending)
    
    Returns:
        dict: Sorted list of patients
    
    Raises:
        HTTPException: If sort_by or order values are invalid
    
    Examples:
        GET /patients/search/sorted?sort_by=weight&order=descending
        GET /patients/search/sorted?sort_by=bmi&order=ascending
        GET /patients/search/sorted (uses defaults)
    """
    # Valid fields for sorting
    valid_fields = ["id", "weight", "height", "bmi", "age"]
    valid_orders = ["ascending", "descending"]
    
    # Validate sort_by parameter
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort field: '{sort_by}'. Valid fields: {', '.join(valid_fields)}"
        )
    
    # Validate order parameter
    if order not in valid_orders:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid order: '{order}'. Valid orders: {', '.join(valid_orders)}"
        )
    
    # Load and sort patients
    patients = load_patients_data()
    patients_list = list(patients.values())
    
    # Determine sort key
    reverse = order == "descending"
    
    # Sort by specified field
    sorted_patients = sorted(
        patients_list,
        key=lambda p: p.get(sort_by, 0),
        reverse=reverse
    )
    
    return {
        "status": "success",
        "sorting": {
            "field": sort_by,
            "order": order
        },
        "total": len(sorted_patients),
        "patients": sorted_patients
    }


@app.get("/patients/search/by-field", tags=["Patients", "Filtering"])
async def search_by_field(
    field: str = Query(
        ...,
        title="Search Field",
        description="Field to search in (name, age, weight)",
        example="name"
    ),
    value: str = Query(
        ...,
        title="Search Value",
        description="Value to search for",
        example="Rajesh"
    )
):
    """
    Search patients by a specific field value.
    
    This endpoint demonstrates:
    - Required query parameters (using ... in Query())
    - Filtering based on user input
    - Flexible search across different fields
    
    Args:
        field (str): Field to search in (name, age, weight)
        value (str): Value to search for
    
    HTTP Status Codes:
    - 200: Search completed (even if no results)
    - 400: Invalid field specified
    
    Returns:
        dict: List of matching patients
    
    Raises:
        HTTPException: If field is invalid
    
    Examples:
        GET /patients/search/by-field?field=name&value=Rajesh
        GET /patients/search/by-field?field=age&value=30
    """
    valid_fields = ["name", "age", "weight", "height"]
    
    if field not in valid_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid search field: '{field}'. Valid fields: {', '.join(valid_fields)}"
        )
    
    patients = load_patients_data()
    
    # Search for matching patients
    matching = []
    for patient in patients.values():
        patient_value = str(patient.get(field, "")).lower()
        search_value = str(value).lower()
        
        if search_value in patient_value:
            matching.append(patient)
    
    return {
        "status": "success",
        "search": {
            "field": field,
            "value": value
        },
        "found": len(matching),
        "patients": matching
    }


# ============================================================================
# COMBINED PATH & QUERY PARAMETERS
# ============================================================================

@app.get("/patients/{patient_id}/details", tags=["Patients"])
async def get_patient_with_details(
    patient_id: str = Path(
        ...,
        description="Patient ID",
        example="P001"
    ),
    include_stats: bool = Query(
        False,
        description="Include calculated statistics for this patient"
    )
):
    """
    Get detailed patient information with optional statistics.
    
    This endpoint demonstrates:
    - Using both path and query parameters together
    - Path parameter for resource identification
    - Query parameter for optional features
    
    Args:
        patient_id (str): The patient ID (path parameter)
        include_stats (bool): Whether to include calculated stats (query parameter)
    
    HTTP Status Codes:
    - 200: Patient found with details
    - 404: Patient not found
    
    Returns:
        dict: Patient details with optional statistics
    
    Examples:
        GET /patients/P001/details
        GET /patients/P001/details?include_stats=true
    """
    patients = load_patients_data()
    
    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient '{patient_id}' not found"
        )
    
    patient = patients[patient_id]
    response = {
        "status": "success",
        "patient": patient
    }
    
    # Add optional statistics if requested
    if include_stats:
        response["statistics"] = {
            "bmi_category": get_bmi_category(patient.get("bmi", 0)),
            "height_meters": patient.get("height", 0),
            "weight_kg": patient.get("weight", 0),
            "age_group": get_age_group(patient.get("age", 0))
        }
    
    return response


# ============================================================================
# CREATE ENDPOINT - WITH STATUS CODE
# ============================================================================

@app.post("/patients", status_code=status.HTTP_201_CREATED, tags=["Patients"])
async def create_patient(patient_data: dict):
    """
    Create a new patient record.
    
    This endpoint demonstrates:
    - POST method for creating resources
    - 201 Created status code for successful creation
    - Auto-calculating derived fields (BMI, ID)
    - Data validation and error handling
    
    HTTP Status Codes:
    - 201: Patient successfully created
    - 400: Invalid data provided
    
    Args:
        patient_data (dict): Patient information
            Required fields: name, age, height, weight
    
    Returns:
        dict: Newly created patient with auto-generated ID and calculated BMI
    
    Raises:
        HTTPException: If required fields are missing
    
    Example Request Body:
        {
            "name": "Rahul Sharma",
            "age": 28,
            "height": 1.75,
            "weight": 70
        }
    """
    patients = load_patients_data()
    
    # Validate required fields
    required_fields = ["name", "age", "height", "weight"]
    for field in required_fields:
        if field not in patient_data or patient_data[field] is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required field: {field}"
            )
    
    # Generate new patient ID
    max_id = max([int(p["id"].replace("P", "")) for p in patients.values()]) if patients else 0
    new_id = f"P{str(max_id + 1).zfill(3)}"
    
    # Calculate BMI
    bmi = calculate_bmi(patient_data["weight"], patient_data["height"])
    
    # Create new patient record
    new_patient = {
        "id": new_id,
        "name": patient_data["name"],
        "age": patient_data["age"],
        "height": patient_data["height"],
        "weight": patient_data["weight"],
        "bmi": bmi,
        "created_at": datetime.now().isoformat()
    }
    
    # Save to database
    patients[new_id] = new_patient
    save_patients_data(patients)
    
    return {
        "status": "success",
        "message": f"Patient {new_id} created successfully",
        "patient": new_patient
    }


# ============================================================================
# UPDATE ENDPOINT - WITH STATUS CODE
# ============================================================================

@app.patch("/patients/{patient_id}", status_code=status.HTTP_200_OK, tags=["Patients"])
async def update_patient(
    patient_id: str = Path(..., description="Patient ID"),
    patient_data: dict = None
):
    """
    Update a patient's information (partial update).
    
    This endpoint demonstrates:
    - PATCH method for partial updates
    - 200 OK status code for successful update
    - Recalculating BMI when weight/height changes
    - Proper error handling
    
    HTTP Status Codes:
    - 200: Patient successfully updated
    - 404: Patient not found
    - 400: Invalid data
    
    Args:
        patient_id (str): ID of patient to update
        patient_data (dict): Fields to update
    
    Returns:
        dict: Updated patient information
    """
    if patient_data is None:
        patient_data = {}
    
    patients = load_patients_data()
    
    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient '{patient_id}' not found"
        )
    
    patient = patients[patient_id]
    
    # Update fields
    for key, value in patient_data.items():
        if key in ["name", "age", "height", "weight"]:
            patient[key] = value
    
    # Recalculate BMI if weight or height changed
    if "weight" in patient_data or "height" in patient_data:
        patient["bmi"] = calculate_bmi(patient["weight"], patient["height"])
    
    # Save
    save_patients_data(patients)
    
    return {
        "status": "success",
        "message": f"Patient {patient_id} updated successfully",
        "patient": patient
    }


# ============================================================================
# DELETE ENDPOINT - WITH STATUS CODE
# ============================================================================

@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Patients"])
async def delete_patient(
    patient_id: str = Path(..., description="Patient ID")
):
    """
    Delete a patient record.
    
    This endpoint demonstrates:
    - DELETE method for removing resources
    - 204 No Content status code (success with no response body)
    - Proper error handling for missing resources
    
    HTTP Status Codes:
    - 204: Patient successfully deleted (no content returned)
    - 404: Patient not found
    
    Args:
        patient_id (str): ID of patient to delete
    
    Returns:
        None (204 No Content - no response body)
    
    Raises:
        HTTPException: If patient not found
    """
    patients = load_patients_data()
    
    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient '{patient_id}' not found"
        )
    
    # Delete patient
    del patients[patient_id]
    save_patients_data(patients)
    
    # 204 No Content - no return value needed


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_bmi_category(bmi: float) -> str:
    """
    Categorize BMI value.
    
    Args:
        bmi (float): BMI value
    
    Returns:
        str: BMI category
    """
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def get_age_group(age: int) -> str:
    """
    Categorize age into groups.
    
    Args:
        age (int): Age value
    
    Returns:
        str: Age group
    """
    if age < 18:
        return "Minor"
    elif age < 35:
        return "Young Adult"
    elif age < 50:
        return "Middle-aged"
    else:
        return "Senior"


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom exception handler for HTTPException.
    
    Returns a consistent error response format.
    """
    return {
        "status": "error",
        "status_code": exc.status_code,
        "message": exc.detail,
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
