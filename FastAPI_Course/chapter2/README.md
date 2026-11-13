# Chapter 2: HTTP Methods & CRUD Operations - Running Guide

## Overview
This folder contains the complete implementation of a Patient Management System API that demonstrates all HTTP Methods and CRUD operations.

## Files in this Directory

- **chapter2.md** - Comprehensive guide on HTTP Methods, CRUD, and practical examples
- **main.py** - Complete FastAPI application with all CRUD endpoints
- **patients.json** - Sample patient data (database simulation)
- **README.md** - This file

## Quick Start

### Step 1: Navigate to this Directory
```bash
cd /Users/bhandar3/Desktop/personal/backend-machine-coding-prep/FastAPI_Course/chapter2
```

### Step 2: Activate Virtual Environment
```bash
source ../venv/bin/activate  # From chapter2 folder, go up one level to access venv
```

### Step 3: Run the Application
```bash
uvicorn main:app --reload
```

### Step 4: Access the API
- **Swagger UI (Interactive Docs):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc (Alternative Docs):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **API Root:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## API Endpoints & HTTP Methods

### Root Endpoints

#### GET /
```
Description: Welcome message
HTTP Method: GET (Retrieve)
```

#### GET /about
```
Description: API information and features
HTTP Method: GET (Retrieve)
```

### Patient Management Endpoints

#### GET /patients
```
Description: Get all patients
HTTP Method: GET (Retrieve - READ)
CRUD Operation: RETRIEVE

Example:
GET http://127.0.0.1:8000/patients

Response:
{
  "total": 5,
  "patients": [
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
}
```

#### GET /patients/{patient_id}
```
Description: Get specific patient by ID
HTTP Method: GET (Retrieve - READ)
CRUD Operation: RETRIEVE

Example:
GET http://127.0.0.1:8000/patients/1

Response:
{
  "id": 1,
  "name": "Rajesh Kumar",
  "age": 35,
  "height": 180,
  "weight": 75,
  "bmi": 23.15
}
```

#### POST /patients
```
Description: Create new patient record
HTTP Method: POST (Create - CREATE)
CRUD Operation: CREATE

Parameters:
- name (string): Patient's full name
- age (integer): Patient's age
- height (integer): Height in cm
- weight (float): Weight in kg

Example:
POST http://127.0.0.1:8000/patients?name=John Doe&age=30&height=180&weight=70

Response:
{
  "message": "Patient created successfully",
  "patient": {
    "id": 6,
    "name": "John Doe",
    "age": 30,
    "height": 180,
    "weight": 70,
    "bmi": 21.6
  }
}
```

#### PATCH /patients/{patient_id}
```
Description: Partially update patient record
HTTP Method: PATCH (Update - Partial)
CRUD Operation: UPDATE

Parameters (all optional):
- name: Patient's name
- age: Patient's age
- height: Height in cm
- weight: Weight in kg

Example:
PATCH http://127.0.0.1:8000/patients/1?weight=72

Note: Only updates provided fields. BMI recalculated automatically.

Response:
{
  "message": "Patient updated successfully",
  "patient": {
    "id": 1,
    "name": "Rajesh Kumar",
    "age": 35,
    "height": 180,
    "weight": 72,
    "bmi": 22.22
  }
}
```

#### PUT /patients/{patient_id}
```
Description: Fully replace patient record
HTTP Method: PUT (Update - Full Replacement)
CRUD Operation: UPDATE

Parameters (all required):
- name: Patient's full name
- age: Patient's age
- height: Height in cm
- weight: Weight in kg

Example:
PUT http://127.0.0.1:8000/patients/1?name=Rajesh Kumar&age=36&height=180&weight=76

Note: All fields required. Use PATCH for partial updates.

Response:
{
  "message": "Patient record replaced successfully",
  "patient": {
    "id": 1,
    "name": "Rajesh Kumar",
    "age": 36,
    "height": 180,
    "weight": 76,
    "bmi": 23.45
  }
}
```

#### DELETE /patients/{patient_id}
```
Description: Delete patient record
HTTP Method: DELETE (Delete - DELETE)
CRUD Operation: DELETE

Example:
DELETE http://127.0.0.1:8000/patients/1

Response:
{
  "message": "Patient deleted successfully",
  "deleted_patient": {
    "id": 1,
    "name": "Rajesh Kumar",
    "age": 35,
    "height": 180,
    "weight": 75,
    "bmi": 23.15
  }
}
```

### Utility Endpoints

#### GET /stats
```
Description: Get statistics about patients
HTTP Method: GET (Retrieve)

Example:
GET http://127.0.0.1:8000/stats

Response:
{
  "total_patients": 5,
  "average_age": 36.8,
  "average_weight": 72.4,
  "average_bmi": 24.52,
  "age_range": {
    "min": 28,
    "max": 48
  },
  "weight_range": {
    "min": 58,
    "max": 85
  }
}
```

---

## Testing Endpoints

### Using Swagger UI
1. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"
6. View the response

### Using curl Commands

**GET all patients:**
```bash
curl -X GET "http://127.0.0.1:8000/patients"
```

**GET specific patient:**
```bash
curl -X GET "http://127.0.0.1:8000/patients/1"
```

**Create new patient (POST):**
```bash
curl -X POST "http://127.0.0.1:8000/patients?name=Jane%20Doe&age=25&height=165&weight=60"
```

**Update patient (PATCH):**
```bash
curl -X PATCH "http://127.0.0.1:8000/patients/1?weight=72"
```

**Replace patient (PUT):**
```bash
curl -X PUT "http://127.0.0.1:8000/patients/1?name=Rajesh%20Kumar&age=36&height=180&weight=76"
```

**Delete patient (DELETE):**
```bash
curl -X DELETE "http://127.0.0.1:8000/patients/1"
```

---

## HTTP Methods Summary

| Method | Operation | CRUD | Usage |
|--------|-----------|------|-------|
| GET | Retrieve data | R | `GET /patients` |
| POST | Create resource | C | `POST /patients` |
| PATCH | Partial update | U | `PATCH /patients/1` |
| PUT | Full replacement | U | `PUT /patients/1` |
| DELETE | Remove resource | D | `DELETE /patients/1` |

---

## Key Concepts Demonstrated

### ✅ What This Code Shows

1. **GET Requests**
   - Retrieving all resources
   - Retrieving specific resources by ID

2. **POST Requests**
   - Creating new resources
   - Automatic ID generation
   - Data validation

3. **PATCH Requests**
   - Partial updates
   - Only modifying specified fields
   - Automatic recalculation (BMI)

4. **PUT Requests**
   - Full resource replacement
   - All fields required
   - Difference from PATCH

5. **DELETE Requests**
   - Removing resources
   - Confirmation with deleted data

6. **JSON File Operations**
   - Loading data from JSON
   - Saving data to JSON
   - Simulating a database

7. **Error Handling**
   - 404 responses for not found
   - Proper error messages

---

## Understanding the Code

### Key Functions

**load_patients_data()**
- Reads patients.json file
- Returns list of patient dictionaries
- Handles file not found errors

**save_patients_data(patients)**
- Writes patients list to JSON
- Pretty prints with indentation
- Persists data changes

### Key Endpoints Pattern

```python
@app.get("/patients")           # GET - Read all
@app.get("/patients/{id}")      # GET - Read specific
@app.post("/patients")          # POST - Create
@app.patch("/patients/{id}")    # PATCH - Update partial
@app.put("/patients/{id}")      # PUT - Update full
@app.delete("/patients/{id}")   # DELETE - Remove
```

---

## Next Steps

1. **Explore** all endpoints in Swagger UI
2. **Test** CREATE, READ, UPDATE, DELETE operations
3. **Notice** how BMI auto-recalculates on weight changes
4. **Observe** how data persists in patients.json
5. **Read** Chapter 2 markdown for deep understanding
6. **Try** modifying the code (add more fields, new endpoints, etc.)

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:** Activate virtual environment: `source ../venv/bin/activate`

### Issue: "Port 8000 already in use"
**Solution:** Change port: `uvicorn main:app --reload --port 8001`

### Issue: "patients.json not found"
**Solution:** The file will be created automatically on first POST request, or manually create it with sample data

### Issue: "Cannot find venv"
**Solution:** Create it from parent directory:
```bash
cd ..
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn[standard]
```

---

## Learning Path

1. ✅ Read **Chapter 2 markdown** to understand concepts
2. ✅ Run **main.py** and explore endpoints
3. ✅ Test each HTTP method in Swagger UI
4. ✅ Modify code to add new features
5. ✅ Study how CRUD maps to HTTP methods
6. ✅ Learn the difference between PATCH and PUT

---

## Resources

- **FastAPI Docs:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **HTTP Methods:** [https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- **CRUD Operations:** [https://en.wikipedia.org/wiki/Create,_read,_update_and_delete](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)
- **JSON Format:** [https://www.json.org/](https://www.json.org/)

Happy coding! 🚀
