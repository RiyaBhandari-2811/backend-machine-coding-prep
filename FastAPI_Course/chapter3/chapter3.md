# Chapter 3: Path Parameters, Query Parameters & HTTP Status Codes

## Table of Contents
1. [Introduction](#introduction)
2. [Path Parameters](#path-parameters)
3. [Path Function for Validation & Documentation](#path-function-for-validation--documentation)
4. [HTTP Status Codes](#http-status-codes)
5. [HTTPException & Error Handling](#httpexception--error-handling)
6. [Query Parameters](#query-parameters)
7. [Combining Path & Query Parameters](#combining-path--query-parameters)
8. [Practical Examples](#practical-examples)
9. [Interview Questions & Answers](#interview-questions--answers)
10. [Summary](#summary)

---

## Introduction

In this chapter, we'll explore the mechanisms for passing data to API endpoints:
- **Path Parameters** - Dynamic URL segments for identifying specific resources
- **Query Parameters** - Optional data appended to URLs for filtering and sorting
- **HTTP Status Codes** - Standardized responses indicating request results
- **Error Handling** - Proper exception handling with HTTPException

These concepts are essential for building flexible, user-friendly APIs.

---

## Path Parameters

### What are Path Parameters?

**Definition:** Path Parameters are dynamic segments of a URL path used to identify a specific resource.

**Characteristics:**
- Part of the URL path itself
- Required (must be provided)
- Used to specify which resource to operate on
- Change for different requests
- Non-optional

### Path Parameters vs Static URL

```
Static URL:     http://127.0.0.1:8000/patients
                                        └─ Fixed

Dynamic URL:    http://127.0.0.1:8000/patients/5
                                                 └─ Path Parameter (changes per request)

Another call:   http://127.0.0.1:8000/patients/10
                                                 └─ Different Path Parameter value
```

### When to Use Path Parameters

Use path parameters when you need to:
- **Retrieve specific resources** - `GET /patients/5`
- **Update specific resources** - `PATCH /patients/5`
- **Delete specific resources** - `DELETE /patients/5`
- **Access nested resources** - `GET /patients/5/medical-history`

### Path Parameters in FastAPI

```python
from fastapi import FastAPI

app = FastAPI()

# Path parameter declared in curly braces
@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    # patient_id is automatically extracted from URL
    return {"patient_id": patient_id}

# Multiple path parameters
@app.get("/hospitals/{hospital_id}/patients/{patient_id}")
async def get_patient_at_hospital(hospital_id: int, patient_id: int):
    return {
        "hospital_id": hospital_id,
        "patient_id": patient_id
    }
```

### How FastAPI Extracts Path Parameters

```
Request URL: GET /patients/5
                           └─ This "5" is extracted
                           
FastAPI reads the route pattern: /patients/{patient_id}
                                           └─ Matches this placeholder
                                           
The value "5" is passed to function as patient_id parameter
```

### Path Parameter Data Types

FastAPI automatically converts path parameters to the specified type:

```python
@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):  # Converted to integer
    return {"patient_id": patient_id, "type": type(patient_id).__name__}

# If URL: /patients/5
# Returns: {"patient_id": 5, "type": "int"}

# If URL: /patients/abc
# FastAPI automatically rejects (validation error)
```

---

## Path Function for Validation & Documentation

### What is the Path Function?

**Definition:** The `Path` function is a utility provided by FastAPI to declare, validate, and document path parameters in your API endpoints.

**Purpose:**
- Add descriptions for better documentation
- Provide examples for clarity
- Add validation rules (min, max, regex, length)
- Set default values (rarely used with path params)
- Enhance API discoverability

### Importing Path Function

```python
from fastapi import FastAPI, Path
```

### Using Path Function

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: int = Path(
        ...,  # ... means required
        description="ID of the patient in the database",
        example="P001",
        gt=0,  # greater than
        le=1000  # less than or equal to
    )
):
    return {"patient_id": patient_id}
```

### Path Function Parameters

| Parameter | Type | Purpose | Example |
|-----------|------|---------|---------|
| `...` or `Ellipsis` | - | Indicates required parameter | `Path(...)` |
| `description` | str | Human-readable description | `description="Patient ID"` |
| `example` | any | Example value for documentation | `example="P001"` |
| `title` | str | Display title in docs | `title="Patient ID"` |
| `gt` | int/float | Greater than | `gt=0` |
| `ge` | int/float | Greater than or equal | `ge=1` |
| `lt` | int/float | Less than | `lt=1000` |
| `le` | int/float | Less than or equal | `le=999` |
| `min_length` | int | Minimum string length | `min_length=3` |
| `max_length` | int | Maximum string length | `max_length=50` |
| `regex` | str | Pattern to match | `regex="^P[0-9]{3}$"` |

### Complete Example

```python
@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: str = Path(
        ...,
        title="Patient ID",
        description="The unique identifier of the patient",
        example="P001",
        min_length=1,
        max_length=10,
        regex="^P[0-9]{3,4}$"
    )
):
    """
    Get patient details by ID.
    
    - **patient_id**: Must start with 'P' followed by 3-4 digits (e.g., P001)
    """
    return {"patient_id": patient_id}
```

### Benefits in Documentation

When you use Path(), Swagger UI automatically displays:
- Parameter description
- Example values
- Validation constraints
- Data type information

This helps API consumers understand exactly what values to provide.

---

## HTTP Status Codes

### What are HTTP Status Codes?

**Definition:** HTTP Status Codes are three-digit numbers returned by a web server to indicate the result of a client's request.

### The Five Categories

| Range | Meaning | Purpose |
|-------|---------|---------|
| **2xx** | Success | Request was successful |
| **3xx** | Redirection | Further action required |
| **4xx** | Client Error | Client's request is invalid |
| **5xx** | Server Error | Server failed to fulfill valid request |

### Common HTTP Status Codes

#### **2xx - Success**

```
200 OK
- Request succeeded
- Response contains data
- Used by: GET (retrieve data successfully)

201 Created
- New resource created successfully
- Returned with new resource data
- Used by: POST (create new patient)

204 No Content
- Request succeeded but no content to return
- Success without response body
- Used by: DELETE (deleted successfully)
```

#### **3xx - Redirection**

```
301 Moved Permanently
- Resource moved to new location
- Client should update bookmarks

302 Found
- Resource temporarily at different location
- Follow redirect
```

#### **4xx - Client Error**

```
400 Bad Request
- Invalid data in request
- Missing required fields
- Wrong data type

401 Unauthorized
- Authentication required
- User not logged in
- Invalid credentials

403 Forbidden
- User authenticated but not authorized
- Insufficient permissions
- Access denied

404 Not Found
- Resource doesn't exist
- Patient ID doesn't exist
- Endpoint not found
```

#### **5xx - Server Error**

```
500 Internal Server Error
- Server encountered unexpected error
- Bug in application code

502 Bad Gateway
- Server is gateway/proxy
- Received invalid response
- Network issue

503 Service Unavailable
- Server temporarily unavailable
- Maintenance or overloaded
- Try again later
```

### Using Status Codes in FastAPI

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.get("/patients/{patient_id}", status_code=status.HTTP_200_OK)
async def get_patient(patient_id: int):
    return {"patient_id": patient_id}

@app.post("/patients", status_code=status.HTTP_201_CREATED)
async def create_patient(patient_data: dict):
    new_patient = save_patient(patient_data)
    return new_patient

@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int):
    delete_patient_from_db(patient_id)
    # No return needed for 204
```

### Response Status Code Table

| Operation | HTTP Method | Typical Status Code |
|-----------|-------------|-------------------|
| Retrieve data | GET | 200 OK |
| Create resource | POST | 201 Created |
| Update resource | PATCH/PUT | 200 OK |
| Delete resource | DELETE | 204 No Content |
| Invalid request | Any | 400 Bad Request |
| Not found | Any | 404 Not Found |
| Server error | Any | 500 Internal Server Error |

---

## HTTPException & Error Handling

### What is HTTPException?

**Definition:** HTTPException is a special built-in exception in FastAPI that returns custom HTTP error responses with proper status codes and error messages.

**Without HTTPException** (Bad Practice):
```python
@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    if patient_id not in patients_db:
        return {"error": "Patient not found"}  # Status 200 (WRONG!)
```

**Problem:** Returns 200 OK even when patient not found. Client thinks request succeeded!

**With HTTPException** (Good Practice):
```python
from fastapi import HTTPException

@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )  # Status 404 (CORRECT!)
```

### HTTPException Syntax

```python
from fastapi import HTTPException

raise HTTPException(
    status_code: int,          # HTTP status code (400, 404, 500, etc.)
    detail: str = None,        # Error message for client
    headers: dict = None       # Optional response headers
)
```

### Common HTTPException Examples

```python
# 400 Bad Request
raise HTTPException(
    status_code=400,
    detail="Invalid patient ID. ID must be numeric."
)

# 404 Not Found
raise HTTPException(
    status_code=404,
    detail="Patient with ID 999 not found in database"
)

# 401 Unauthorized
raise HTTPException(
    status_code=401,
    detail="Authentication required. Please log in."
)

# 403 Forbidden
raise HTTPException(
    status_code=403,
    detail="You don't have permission to access this resource"
)

# 500 Internal Server Error
raise HTTPException(
    status_code=500,
    detail="Database connection failed. Please try again later."
)
```

### Error Handling Example

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    # Check if patient exists
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=404,
            detail=f"Patient with ID {patient_id} not found"
        )
    
    # Check if patient is active
    if not patients_db[patient_id].is_active:
        raise HTTPException(
            status_code=403,
            detail="Patient record is archived"
        )
    
    return patients_db[patient_id]
```

---

## Query Parameters

### What are Query Parameters?

**Definition:** Query Parameters are optional key-value pairs appended to the end of a URL, used to pass additional data to the server for filtering, sorting, searching, and pagination.

**Structure:**
```
URL Format: http://api.example.com/patients?sort_by=weight&order=ascending
                                            │ Question mark starts query
                                            │ 
                                            └─ sort_by=weight (first parameter)
                                                          │
                                                          └─ order=ascending (second parameter, separated by &)
```

### Query Parameters vs Path Parameters

| Aspect | Path Parameters | Query Parameters |
|--------|-----------------|------------------|
| **Location** | Part of URL path | After ? in URL |
| **Required** | Required | Optional |
| **Use Case** | Identify specific resource | Filter/sort data |
| **Example** | `/patients/5` | `/patients?age=30&city=Delhi` |
| **Multiplicity** | One per segment | Multiple possible |

### Declaring Query Parameters

```python
from fastapi import FastAPI, Query

app = FastAPI()

# Simple query parameter
@app.get("/patients")
async def get_patients(skip: int = 0, limit: int = 10):
    # skip and limit are query parameters
    # Default values: skip=0, limit=10
    return {"skip": skip, "limit": limit}

# With Query function
@app.get("/patients")
async def get_patients(
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return")
):
    return {"skip": skip, "limit": limit}
```

### Using Query Parameters

```
GET /patients                               # Use defaults: skip=0, limit=10
GET /patients?skip=5                        # Override skip: skip=5, limit=10
GET /patients?limit=20                      # Override limit: skip=0, limit=20
GET /patients?skip=5&limit=20              # Override both
GET /patients?skip=0&limit=10&sort_by=age # Multiple parameters
```

### Query Function Parameters

| Parameter | Type | Purpose | Example |
|-----------|------|---------|---------|
| Default | any | Default value if not provided | `Query(0)` |
| `description` | str | Parameter description | `description="Skip X records"` |
| `example` | any | Example value | `example=10` |
| `title` | str | Display name | `title="Limit"` |
| `ge` | int/float | Greater than or equal | `ge=1` |
| `le` | int/float | Less than or equal | `le=100` |
| `min_length` | int | Minimum length | `min_length=3` |
| `max_length` | int | Maximum length | `max_length=50` |
| `regex` | str | Pattern match | `regex="^[a-z]+$"` |
| `deprecated` | bool | Mark as deprecated | `deprecated=True` |

### Query Parameters for Sorting and Filtering

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/patients")
async def get_patients(
    sort_by: str = Query(
        "id",
        description="Sort by: id, weight, height, or bmi",
        example="weight"
    ),
    order: str = Query(
        "ascending",
        description="Order: ascending or descending",
        example="ascending"
    ),
    min_age: int = Query(None, ge=0, description="Minimum age"),
    max_age: int = Query(None, le=120, description="Maximum age")
):
    # Filter and sort logic
    patients = load_patients()
    
    # Apply filters
    if min_age:
        patients = [p for p in patients if p.age >= min_age]
    if max_age:
        patients = [p for p in patients if p.age <= max_age]
    
    # Apply sorting
    reverse = order == "descending"
    patients = sorted(patients, key=lambda p: getattr(p, sort_by), reverse=reverse)
    
    return patients
```

---

## Combining Path & Query Parameters

### Using Both Together

You can use path parameters for resource identification and query parameters for filtering/sorting:

```python
@app.get("/hospitals/{hospital_id}/patients")
async def get_hospital_patients(
    hospital_id: int = Path(..., description="Hospital ID"),
    age: int = Query(None, description="Filter by age"),
    sort_by: str = Query("id", description="Sort field"),
    order: str = Query("ascending", description="Sort order")
):
    """
    Get all patients in a specific hospital with optional filtering and sorting.
    
    - **hospital_id** (path): Which hospital's patients to retrieve (required)
    - **age** (query): Filter patients by age (optional)
    - **sort_by** (query): Sort by field (optional)
    - **order** (query): Sort direction (optional)
    """
    return {
        "hospital_id": hospital_id,
        "filters": {"age": age},
        "sorting": {"by": sort_by, "order": order}
    }
```

### URL Examples

```
GET /hospitals/1/patients
└─ All patients in hospital 1

GET /hospitals/1/patients?age=30
└─ Patients in hospital 1 aged 30

GET /hospitals/1/patients?sort_by=weight&order=descending
└─ Patients in hospital 1 sorted by weight descending

GET /hospitals/1/patients?age=30&sort_by=weight&order=ascending
└─ Patients in hospital 1 aged 30, sorted by weight ascending
```

---

## Practical Examples

### Example 1: Complete Patient Retrieval Endpoint

```python
from fastapi import FastAPI, Path, Query, HTTPException

app = FastAPI()

@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: str = Path(
        ...,
        description="Unique patient identifier",
        example="P001",
        regex="^P[0-9]{3}$"
    )
):
    """Get a specific patient by ID."""
    patient = find_patient_by_id(patient_id)
    
    if not patient:
        raise HTTPException(
            status_code=404,
            detail=f"Patient {patient_id} not found"
        )
    
    return patient
```

### Example 2: Listing with Sorting

```python
@app.get("/patients")
async def list_patients(
    sort_by: str = Query(
        "id",
        description="Sort by: id, weight, height, or bmi",
        regex="^(id|weight|height|bmi)$"
    ),
    order: str = Query(
        "ascending",
        description="Order: ascending or descending",
        regex="^(ascending|descending)$"
    ),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records per page")
):
    """List all patients with sorting and pagination."""
    patients = load_all_patients()
    
    # Validate sort field
    if sort_by not in ["id", "weight", "height", "bmi"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field: {sort_by}"
        )
    
    # Sort
    reverse = order == "descending"
    sorted_patients = sorted(
        patients,
        key=lambda p: getattr(p, sort_by),
        reverse=reverse
    )
    
    # Paginate
    paginated = sorted_patients[skip:skip+limit]
    
    return {
        "total": len(patients),
        "returned": len(paginated),
        "patients": paginated
    }
```

---

## Interview Questions & Answers

### Q1: What is the difference between path parameters and query parameters?

**Answer:**

| Aspect | Path Parameters | Query Parameters |
|--------|-----------------|------------------|
| **Location** | Part of URL path | Appended after ? |
| **Required** | Required | Optional |
| **Use** | Identify resource | Filter/sort/paginate |
| **Example** | `/patients/5` | `/patients?age=30` |
| **URL** | `/resource/{id}` | `/resource?key=value` |

**Path Parameter Example:**
```
GET /patients/5  ← Identify patient #5 (required)
```

**Query Parameter Example:**
```
GET /patients?age=30&city=Delhi  ← Filter by age and city (optional)
```

### Q2: When should I use path parameters vs query parameters?

**Answer:**

Use **Path Parameters** when:
- Identifying a specific resource (required)
- Resource is unique/singular
- Example: `/patients/5`, `/hospitals/10/wards/3`

Use **Query Parameters** when:
- Filtering results (optional)
- Sorting or pagination needed
- Multiple variations of same endpoint
- Example: `/patients?age=30&sort_by=weight`

### Q3: What does the Path() function do and why use it?

**Answer:**

The `Path()` function provides:
1. **Validation** - Ensure values match constraints (min, max, regex)
2. **Documentation** - Add descriptions and examples to Swagger UI
3. **Better UX** - API consumers see what values are valid

```python
# Without Path() - No validation or docs
@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    pass

# With Path() - Validation and docs
@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: int = Path(..., gt=0, le=9999, example=5)
):
    pass
```

### Q4: What are HTTP status codes and why are they important?

**Answer:**

HTTP status codes are 3-digit numbers indicating request results:

- **2xx (Success)** - Request succeeded (200 OK, 201 Created)
- **3xx (Redirect)** - Further action needed (301 Moved)
- **4xx (Client Error)** - Client's fault (400 Bad Request, 404 Not Found)
- **5xx (Server Error)** - Server's fault (500 Internal Error)

**Why important:**
- Inform clients if request succeeded or failed
- Specify type of error for proper handling
- Enable automatic retries and error recovery
- Required for API contract/specification

### Q5: What is HTTPException and when should I use it?

**Answer:**

`HTTPException` returns proper HTTP errors with status codes and messages.

**Without HTTPException** (WRONG):
```python
@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    if patient_id not in db:
        return {"error": "Not found"}  # Returns 200 OK (misleading!)
```

**With HTTPException** (CORRECT):
```python
from fastapi import HTTPException

@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    if patient_id not in db:
        raise HTTPException(status_code=404, detail="Not found")  # Returns 404 (correct!)
```

**When to use:** Whenever request can't be fulfilled normally.

### Q6: How do you validate path parameters with regex?

**Answer:**

Use the `Path()` function with `regex` parameter:

```python
@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: str = Path(
        ...,
        regex="^P[0-9]{3}$"  # P followed by 3 digits
    )
):
    pass

# Valid: P001, P999
# Invalid: P00, PP01, p001
```

### Q7: What's the difference between status code 200 and 201?

**Answer:**

- **200 OK** - Request succeeded, resource retrieved or modified successfully
- **201 Created** - Request succeeded, new resource created successfully

**Usage:**
```python
@app.post("/patients", status_code=201)
async def create_patient(patient: PatientModel):
    new_patient = save_to_db(patient)
    return new_patient  # Return the newly created resource
```

### Q8: How do you implement sorting with query parameters?

**Answer:**

```python
@app.get("/patients")
async def get_patients(
    sort_by: str = Query("id", description="Field to sort by"),
    order: str = Query("ascending", description="Sort order")
):
    patients = load_patients()
    
    # Validate
    if sort_by not in ["id", "weight", "height"]:
        raise HTTPException(400, "Invalid sort_by field")
    
    if order not in ["ascending", "descending"]:
        raise HTTPException(400, "Invalid order")
    
    # Sort
    reverse = order == "descending"
    return sorted(patients, key=lambda p: getattr(p, sort_by), reverse=reverse)
```

### Q9: What happens if a query parameter isn't provided?

**Answer:**

Query parameters are **optional** by default. If not provided, the default value is used:

```python
@app.get("/patients")
async def get_patients(
    skip: int = 0,      # Default: 0
    limit: int = 10     # Default: 10
):
    pass

# GET /patients          → skip=0, limit=10 (both defaults)
# GET /patients?skip=5   → skip=5, limit=10 (skip overridden)
# GET /patients?skip=5&limit=20  → skip=5, limit=20 (both overridden)
```

### Q10: How do you make a query parameter required?

**Answer:**

Use `Query()` without a default value:

```python
from fastapi import Query

@app.get("/patients")
async def search_patients(
    name: str = Query(..., description="Patient name (required)")
):
    # name is required
    pass

# GET /patients         → Error (name required)
# GET /patients?name=John → Works (name provided)
```

---

## 🤔 Confusing Questions (Follow-Up Interview Questions)

These are tricky questions interviewers ask to test deep understanding:

### Q11: What happens if I don't use `...` in Path()? What if I just write Path()?

**Answer:**

If you remove `...` and don't provide a default, the parameter becomes **optional with None as default**:

```python
# ❌ WRONG - Confusing behavior
@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: int = Path()  # Missing ... and default!
):
    return {"patient_id": patient_id}

# This COMPILES but:
# - patient_id becomes optional
# - Default value is None
# - But URL still requires it: /patients/{patient_id}
# - Creates confusing behavior!
```

**Proper ways:**

```python
# ✅ Required
@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: int = Path(...)  # Explicitly required
):
    pass

# ✅ Optional (but rare for path params)
@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: int = Path(default=None)
):
    pass
```

**Rule:** Always explicitly use `...` for required or provide a `default` value!

---

### Q12: Why don't we use the `new` keyword like `new Path(...)`? Why is it different from Java/C++?

**Answer:**

Python is **dynamically typed** and **doesn't require constructors** like Java or C++.

**Java (with `new`):**
```java
Path myPath = new Path(...);  // Java requires 'new'
```

**Python (no `new` needed):**
```python
patient_id: int = Path(...)  # Python - no 'new' keyword needed
```

**Why the difference:**

1. **Python is not compiled** - No need to explicitly allocate memory with `new`
2. **Function calls create objects** - `Path(...)` is a function call that returns an object automatically
3. **Syntactic sugar** - Python treats class instantiation like function calls

**What's actually happening:**
```python
# Python automatically calls __init__() and __new__()
Path(...)  # Is equivalent to: Path.__call__(...)
           # Which creates and returns Path object

# In Java you must be explicit:
new Path(...)  // Must explicitly say "create new instance"
```

**Other Python examples:**
```python
# All of these create objects WITHOUT 'new'
my_list = list()
my_dict = dict()
my_set = set()
my_path = Path(...)
```

**Key Takeaway:** Python doesn't need `new` because it handles object creation automatically!

---

### Q13: What happens if I provide BOTH `...` AND a default value in Path()?

**Answer:**

You **cannot provide both** - it causes an error! FastAPI will reject it:

```python
# ❌ ERROR - Cannot have both ... and default
@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: int = Path(..., default=5)  # INVALID!
):
    pass

# Error: "Cannot specify both ... and default value"
```

**Why?** They are **mutually exclusive**:

- `...` means "required" - no default
- `default=value` means "optional" - has default

**It's like saying:** "Required AND optional" - contradiction!

```python
# ✅ CORRECT - Choose ONE:

# Option 1: Required (use ...)
patient_id: int = Path(...)

# Option 2: Optional (use default)
patient_id: int = Path(default=5)
```

---

### Q14: Can I make path parameters optional? What if I want `/patients` and `/patients/5` to both work?

**Answer:**

**Short answer:** Don't do it. Path parameters are always required.

**Why:** Path parameters are for **resource identification**, not filtering. They should always be required.

**If you need optional:**

Create **separate endpoints** (better design):

```python
# ✅ CORRECT - Two separate endpoints
@app.get("/patients")
async def list_all_patients():
    """Get all patients (no ID needed)"""
    return {"patients": [...]}

@app.get("/patients/{patient_id}")
async def get_single_patient(
    patient_id: int = Path(..., gt=0)
):
    """Get specific patient (ID required)"""
    return {"patient_id": patient_id}

# URLs:
# /patients        → List all
# /patients/5      → Get patient 5
```

**Wrong way (don't do this):**

```python
# ❌ WRONG - Trying to make path param optional
@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: int = Path(default=None)  # Awkward!
):
    if patient_id is None:
        return {"patients": [...]}
    return {"patient_id": patient_id}

# Problem: URL /patients doesn't match route /patients/{patient_id}
# Will return 404 Not Found!
```

**Use Query Parameters for optional:**

```python
# ✅ CORRECT - Query params for optional filters
@app.get("/patients")
async def get_patients(
    patient_id: int = Query(None, description="Optional filter")
):
    if patient_id:
        return {"patient_id": patient_id}
    return {"patients": [...]}

# URLs:
# /patients              → All patients
# /patients?patient_id=5 → Filter by patient_id
```

---

### Q15: What's the difference between `Path(...)` and `Path(default=None)`?

**Answer:**

| Aspect | `Path(...)` | `Path(default=None)` |
|--------|------------|-------------------|
| **Required?** | YES ✅ | NO ❌ |
| **User must provide?** | YES | NO |
| **Default value** | None (no default) | None |
| **When not provided** | Returns 400 error | Uses None value |
| **Use case** | Resource identification | Optional parameters |

**Example:**

```python
# Required - MUST be provided
@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: int = Path(...)
):
    pass

# URL: /patients/5      ✅ Works
# URL: /patients/       ❌ Error 400


# Optional - Can be omitted
@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: int = Path(default=None)
):
    pass

# URL: /patients/5      ✅ Works (patient_id=5)
# URL: /patients/       ✅ Works (patient_id=None)
```

**Real-world confusion:**

Developers coming from other frameworks often think:
```python
# ❌ Thinking: "This should be optional"
patient_id: int = Path(...)

# ✓ Reality: "This is REQUIRED"
# FastAPI will return 400 if not provided
```

---

### Q16: What happens if I send a string value for an integer path parameter?

**Answer:**

FastAPI **automatically validates** and **rejects it** with a 422 error:

```python
@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: int = Path(...)
):
    return {"patient_id": patient_id}

# Request: GET /patients/5
# ✅ Works: patient_id=5 (integer)

# Request: GET /patients/abc
# ❌ Error 422: "value is not a valid integer"
```

**FastAPI does automatic type coercion:**

```python
# Works (string "5" → integer 5)
GET /patients/5        → patient_id=5

# Fails (string "abc" cannot convert to integer)
GET /patients/abc      → Error 422

# Complex type validation
@app.get("/hospitals/{hospital_id}")
async def get_hospital(
    hospital_id: int = Path(..., gt=0, le=1000)
):
    pass

GET /hospitals/500     → ✅ Works
GET /hospitals/-5      → ❌ Error 422 (violates gt=0)
GET /hospitals/5000    → ❌ Error 422 (violates le=1000)
GET /hospitals/abc     → ❌ Error 422 (not integer)
```

**This is automatic validation!** No extra code needed.

---

### Q17: Why does FastAPI require `...` instead of something more readable like `required=True`?

**Answer:**

It's a **Pydantic convention** carried over to FastAPI.

**Historical reason:**

Pydantic (data validation library) uses `...` (Ellipsis) for required fields:

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name: str  # Required (no default)
    age: int   # Required (no default)
    city: str = "Unknown"  # Optional (has default)

# In Path/Query, FastAPI mirrors this pattern:
from fastapi import Path, Query

patient_id: int = Path(...)  # Mirrors Pydantic's "required" concept
```

**Why `...` instead of `required=True`?**

1. **Consistency** - Matches Pydantic's design
2. **Brevity** - `...` is shorter than `required=True`
3. **Pythonic** - Ellipsis (`...`) is valid Python syntax
4. **Legacy** - FastAPI copied Pydantic's approach

**Other frameworks:**

```javascript
// JavaScript - More readable
Path(required: true)

// FastAPI - Following Pydantic
Path(...)
```

**You could argue:** `required=True` is more readable, but `...` is Pythonic tradition.

---

### Q18: What happens if I use Path() for query parameters instead of Query()?

**Answer:**

**Short answer:** It doesn't work as intended. Use `Query()` for query parameters!

```python
# ❌ WRONG - Using Path for query parameter
@app.get("/patients")
async def get_patients(
    age: int = Path(...)  # Wrong!
):
    pass

# Problem: FastAPI expects path parameter {age} in URL
# URL: /patients          → Error (missing path param)
# URL: /patients/30       → Works but confusing!


# ✅ CORRECT - Use Query for query parameters
@app.get("/patients")
async def get_patients(
    age: int = Query(...)  # Correct!
):
    pass

# URL: /patients?age=30   ✅ Works!
```

**Why the difference?**

- **Path()** - Parameter comes from URL path: `/patients/{id}`
- **Query()** - Parameter comes from query string: `/patients?id=5`
- **FastAPI knows** where to look based on function signature

**Mixing them up is a common mistake!**

```python
@app.get("/hospitals/{hospital_id}/patients")
async def get_hospital_patients(
    hospital_id: int = Path(...),           # From path: /hospitals/1/patients
    age: int = Query(None),                 # From query: ?age=30
    sort_by: str = Query("id")              # From query: ?sort_by=weight
):
    pass

# ✅ Correct usage:
# /hospitals/1/patients?age=30&sort_by=weight
```

---

### Q19: If I define a path parameter but don't use it in the function, what happens?

**Answer:**

You get a **validation error** - unused parameters are not allowed!

```python
# ❌ ERROR - Declared but not used
@app.get("/patients/{patient_id}")
async def get_patients(
    age: int = Query(...)  # Different parameter, patient_id not used!
):
    pass

# Error: "path_id in path but not defined in function parameters"
```

**Must match URL declaration with function parameters:**

```python
# ✅ CORRECT
@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: int = Path(...)  # Must match URL {patient_id}
):
    return {"patient_id": patient_id}
```

**Nested example:**

```python
# ✅ CORRECT - All path params used
@app.get("/hospitals/{hospital_id}/wards/{ward_id}/patients/{patient_id}")
async def get_patient(
    hospital_id: int = Path(...),
    ward_id: int = Path(...),
    patient_id: int = Path(...)
):
    return {
        "hospital_id": hospital_id,
        "ward_id": ward_id,
        "patient_id": patient_id
    }
```

---

### Q20: Why do we need to import Path and Query separately? Can't they be the same function?

**Answer:**

They **could technically** be the same function, but they're **separated for clarity**:

```python
# Current (Separate) - GOOD
from fastapi import Path, Query

patient_id: int = Path(...)    # Clear: from URL path
age: int = Query(...)          # Clear: from query string


# Could do this (Combined) - CONFUSING
from fastapi import Param

patient_id: int = Param(..., in_="path")
age: int = Param(..., in_="query")


# Or this (No distinction) - BAD
patient_id: int = FastAPIParam(...)  # Where does it come from?
```

**Why separate?**

1. **Developer Intent** - `Path()` vs `Query()` shows where data comes from
2. **Documentation** - Swagger UI can show different sections
3. **Validation Rules** - Path/Query have different defaults and rules
4. **Error Messages** - Clear where validation failed
5. **Best Practices** - Explicit is better than implicit (Pythonic)

**Under the hood:** Path and Query probably inherit from the same base class!

```python
# Likely implementation (simplified)
class Param:
    def __init__(self, ..., in_location):
        self.in_location = in_location

class Path(Param):
    def __init__(self, ...):
        super().__init__(..., in_location="path")

class Query(Param):
    def __init__(self, ...):
        super().__init__(..., in_location="query")
```

**Key Takeaway:** Separation makes code **clearer and more maintainable**!

---

## Summary

- **Path Parameters** identify specific resources in the URL path (required)
- **Query Parameters** filter/sort/paginate data appended after ? (optional)
- **Path() function** adds validation and documentation to path parameters
- **Query() function** adds validation and documentation to query parameters
- **HTTP Status Codes** indicate request success (2xx), redirect (3xx), client error (4xx), or server error (5xx)
- **HTTPException** raises proper HTTP errors with correct status codes and messages
- **Combine both** path and query parameters for powerful, flexible APIs

In the next chapter, we'll implement **Request Bodies and Data Validation** using Pydantic models!

---

## Additional Resources

### Quick Reference: Common Operations

```
# Get all patients
GET /patients

# Get patients with filtering
GET /patients?age=30&city=Delhi

# Get all patients sorted
GET /patients?sort_by=weight&order=descending

# Get specific patient
GET /patients/P001

# Update specific patient
PATCH /patients/P001?weight=72

# Delete specific patient
DELETE /patients/P001
```

### HTTP Status Code Quick Lookup

```
2xx Success
- 200: OK - Request succeeded
- 201: Created - New resource created
- 204: No Content - Success, no response body

4xx Client Error
- 400: Bad Request - Invalid data
- 401: Unauthorized - Auth required
- 403: Forbidden - No permission
- 404: Not Found - Resource doesn't exist

5xx Server Error
- 500: Internal Error - Server bug
- 502: Bad Gateway - Network error
- 503: Unavailable - Server overloaded
```

### Path vs Query Parameters Decision Tree

```
Need to identify specific resource?
├─ YES → Use Path Parameter (/patients/5)
└─ NO → Use Query Parameter (/patients?age=30)

Is the parameter required?
├─ YES → Path Parameter (required by nature)
└─ NO → Query Parameter (optional by default)

Multiple variations of same endpoint?
├─ YES → Query Parameter (/patients?sort_by=age)
└─ NO → Path Parameter (/patients/5)
```
