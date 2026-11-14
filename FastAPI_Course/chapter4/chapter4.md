# Chapter 4: POST Endpoint - Creating Records (CREATE in CRUD)

## Overview

After learning to **retrieve** patient data (Chapter 3), we now learn to **create** new patients. This covers the CREATE operation in CRUD.

**What you'll learn:**
- HTTP POST requests vs GET requests
- Request body concept
- Pydantic models for request validation
- Computed fields (BMI, verdict auto-calculation)
- HTTP status codes: 201 (Created), 400 (Bad Request)
- Duplicate prevention

---

## HTTP Methods: GET vs POST

### GET Request (Retrieval)

```
GET /patients
GET /patients/1
GET /patients/sorted?sort_by=age
```

**Purpose:** Retrieve data from server  
**Data Location:** URL (path/query parameters)  
**Idempotent:** Yes (doesn't change server state)

### POST Request (Creation)

```
POST /patients
```

**Purpose:** Create new resource on server  
**Data Location:** Request body (JSON)  
**Idempotent:** No (creates new resource each time)

**Key Difference:** POST sends data **TO** the server, GET retrieves data **FROM** the server.

---

## Request Body

### What is a Request Body?

**Definition:** The portion of an HTTP request that contains data sent by the client to the server.

**Used in:** POST, PUT, PATCH methods (whenever you send data to server)

**Format:** Typically JSON

### Example Request Body

```json
{
  "patient_id": "P006",
  "name": "Rahul Gupta",
  "city": "Hyderabad",
  "age": 19,
  "gender": "Male",
  "height": 1.74,
  "weight": 55
}
```

**Note:** BMI and verdict are **NOT** in the request body - they're calculated server-side.

---

## Pydantic Model for Request Body

### Why Pydantic?

Validates incoming data **before** processing:
- Type checking (age must be int, not string)
- Range validation (age 0-150)
- Constraint validation (weight must be positive)
- Auto-conversion (string "30" → int 30)

### Patient Model with Validation

```python
from pydantic import BaseModel, Field
from typing import Literal

class Patient(BaseModel):
    patient_id: str = Field(..., description="Patient ID (e.g., P001)")
    name: str = Field(..., min_length=1, description="Patient name")
    city: str = Field(..., description="City of residence")
    age: int = Field(..., gt=0, le=150, description="Age in years")
    gender: Literal["Male", "Female", "Others"] = Field(...)
    height: float = Field(..., gt=0, description="Height in meters")
    weight: float = Field(..., gt=0, description="Weight in kg")
```

**Constraints Applied:**
- All fields required (`...`)
- `age`: Must be 0 < age ≤ 150
- `height`, `weight`: Must be positive
- `gender`: Only these 3 options allowed

---

## Computed Fields

### BMI Calculation

**Formula:** BMI = weight / (height²)

```python
from pydantic import computed_field

class Patient(BaseModel):
    # ... other fields ...
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
```

### Verdict Calculation

**Based on BMI:**
- BMI < 18.5 → "Underweight"
- 18.5 ≤ BMI < 25 → "Normal"
- 25 ≤ BMI < 30 → "Overweight"
- BMI ≥ 30 → "Obese"

```python
@computed_field
@property
def verdict(self) -> str:
    if self.bmi < 18.5:
        return "Underweight"
    elif self.bmi < 25:
        return "Normal"
    elif self.bmi < 30:
        return "Overweight"
    else:
        return "Obese"
```

**Key Point:** Server automatically calculates these. Client doesn't need to provide them.

---

## POST Endpoint Architecture

### Step-by-Step Flow

```
1. Client sends HTTP POST request
   ↓ (with request body containing patient data)
   
2. FastAPI receives data
   ↓
   
3. Pydantic model validates
   - If invalid → return 400 error
   - If valid → continue
   ↓
   
4. Check for duplicates
   - If patient_id exists → return 400 error
   - If new patient → continue
   ↓
   
5. Add to database (JSON file)
   ↓
   
6. Return 201 (Created) response
```

---

## Creating the Endpoint

### Basic Structure

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/create")
def create_patient(patient: Patient):
    # Step 1: Load existing data
    data = load_patients_data()
    
    # Step 2: Check for duplicate
    if patient.patient_id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    # Step 3: Convert Pydantic model to dict
    patient_dict = patient.model_dump(exclude={"patient_id"})
    
    # Step 4: Add to database
    data[patient.patient_id] = patient_dict
    
    # Step 5: Save to file
    save_patients_data(data)
    
    # Step 6: Return success response
    return JSONResponse(
        status_code=201,
        content={"message": "Patient created successfully"}
    )
```

---

## HTTP Status Codes

### 201 Created

**When:** Resource successfully created  
**Example:** New patient added to database  
**Response:**
```json
{
  "message": "Patient created successfully"
}
```

### 400 Bad Request

**When:** 
- Invalid data (type mismatch, out of range)
- Duplicate resource (patient_id already exists)

**Pydantic Example (age as string):**
```
ValidationError: age must be a valid integer
```

**Custom Validation Example:**
```json
{
  "detail": "Patient already exists"
}
```

---

## Important Concepts

### Request Body vs Path/Query Parameters

| Aspect | Path Parameter | Query Parameter | Request Body |
|--------|---|---|---|
| Purpose | Single resource ID | Filtering/Sorting | Complex data |
| Example | `/patients/P001` | `/patients?sort=age` | POST with JSON |
| HTTP Method | GET, DELETE | GET | POST, PUT, PATCH |
| Multiple Values | Hard | Easy | Easy |

### Pydantic Model's Role

1. **Validation** - Enforces constraints
2. **Type Conversion** - String to int (when possible)
3. **Documentation** - Auto-generated Swagger docs
4. **Serialization** - Converts to JSON/dict

### Why Computed Fields?

✅ **Single Source of Truth** - BMI calculated from height/weight only once  
✅ **Consistency** - Same calculation everywhere  
✅ **Simplicity** - Client doesn't need to calculate  
✅ **Error Prevention** - No manual calculation errors  

---

## Common Patterns

### Pattern 1: Duplicate Prevention

```python
if patient.patient_id in existing_data:
    raise HTTPException(status_code=400, detail="Duplicate patient ID")
```

### Pattern 2: Auto-increment ID

```python
# Instead of client providing ID
last_id = max([int(p_id[1:]) for p_id in data.keys()]) or 0
new_id = f"P{last_id + 1:03d}"
```

### Pattern 3: Timestamp Auto-addition

```python
from datetime import datetime

@computed_field
@property
def created_at(self) -> str:
    return datetime.now().isoformat()
```

---

## Interview Questions

**Q1: What's the difference between GET and POST?**
A: GET retrieves data from server (idempotent), POST sends data to server to create resources (not idempotent).

**Q2: What is a request body?**
A: The data sent from client to server in POST/PUT/PATCH requests, typically in JSON format.

**Q3: Why use Pydantic models?**
A: Automatic validation, type checking, error messages, and documentation generation.

**Q4: What does status code 201 mean?**
A: Resource successfully created on server.

**Q5: Can client calculate BMI and send it in request?**
A: Technically yes, but it's bad practice. Server should calculate it to ensure accuracy.

**Q6: How do you prevent duplicate patient IDs?**
A: Check if patient_id exists in database before creating. If exists, return 400 error.

**Q7: What happens if age is sent as string "30" instead of int?**
A: Pydantic will try to convert it. If successful, no error. If it fails, return validation error.

**Q8: Why exclude patient_id when converting to dict?**
A: Because we already use patient_id as the dictionary key. We don't need it duplicated in the value.

**Q9: What does model_dump() do?**
A: Converts Pydantic model to Python dictionary. Includes computed fields automatically.

**Q10: Can you modify the patient data after creation?**
A: Yes, but that requires PUT/PATCH endpoints (Update operation, covered later).

---

## Summary

✅ **POST for Creation** - Use POST method for creating resources  
✅ **Request Body** - Send complex data in JSON format  
✅ **Pydantic Validation** - Automatic type checking and constraints  
✅ **Computed Fields** - Server calculates derived values  
✅ **Duplicate Prevention** - Check before creating  
✅ **201 Status Code** - Return when resource created successfully  

---

## Next Chapter (5)

Will cover:
- PUT endpoint for full updates
- PATCH endpoint for partial updates
- Update validation patterns

👉 Start with `main.py` to see working code examples!
