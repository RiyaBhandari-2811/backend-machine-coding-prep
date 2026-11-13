# Chapter 5: PUT & DELETE Endpoints - Update & Delete Records (UPDATE & DELETE in CRUD)

## Overview

After learning to **create and retrieve** patient data (Chapters 3-4), we now complete CRUD with **update** and **delete** operations.

**What you'll learn:**
- PUT method for full/partial updates
- DELETE method for removing resources
- Optional fields in request body (partial updates)
- Recalculating computed fields on update
- HTTP status codes: 200 (OK), 404 (Not Found)
- Path parameters for resource identification

---

## CRUD Operations Summary

| Operation | HTTP Method | Purpose | Status Code |
|-----------|---|---|---|
| **C**reate | POST | Add new resource | 201 Created |
| **R**etrieve | GET | Fetch resource(s) | 200 OK |
| **U**pdate | PUT | Modify existing resource | 200 OK |
| **D**elete | DELETE | Remove resource | 200 OK / 204 No Content |

---

## PUT vs POST

### POST (Create)
```
POST /patients
Request Body: New patient data
Response: 201 Created
Side effect: Creates new resource
```

### PUT (Update)
```
PUT /patients/{patient_id}
Request Body: Updated fields
Response: 200 OK
Side effect: Modifies existing resource
```

**Key Difference:** POST creates new, PUT modifies existing.

---

## Update Endpoint Architecture

### Two Inputs Required

**1. Path Parameter:** Which patient to update
```
PUT /patients/{patient_id}
```

**2. Request Body:** What to update
```json
{
  "city": "Mumbai",
  "weight": 90
}
```

**Note:** Only send fields that changed!

---

## Partial Updates Challenge

### Problem

Patient model requires all fields. But users want to update only 1-2 fields.

### Solution: Optional Fields Model

```python
from typing import Optional

class PatientUpdate(BaseModel):
    """Model for partial updates - all fields optional."""
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Literal["Male", "Female", "Others"]] = None
    height: Optional[float] = None
    weight: Optional[float] = None
```

**Key:** All fields are `Optional[type] = None`

### Benefits

✅ User can send 1 field or 10 fields  
✅ Validation still applies (if sent)  
✅ Server treats missing fields as "don't update"  

---

## Update Logic Flow

### Step-by-Step

```
1. Receive patient_id (path param) + update data (body)
   ↓
2. Load all existing patients from database
   ↓
3. Check if patient_id exists (→ 404 if not)
   ↓
4. Extract existing patient data
   ↓
5. Merge: existing data + new updates
   ↓
6. Recalculate computed fields (BMI, verdict)
   ↓
7. Save to database
   ↓
8. Return 200 OK response
```

### Recalculating Computed Fields

**Challenge:** When weight changes, BMI & verdict become stale.

**Solution:** Convert to Pydantic, then back to dict

```python
# Step 1: Add patient_id back (required by Patient model)
existing_data["patient_id"] = patient_id

# Step 2: Create Pydantic object (recalculates BMI & verdict)
patient_obj = Patient(**existing_data)

# Step 3: Convert back to dict (with new computed values)
updated_data = patient_obj.model_dump(exclude={"patient_id"})
```

### Exclude Unset Pattern

```python
# Convert update model to dict
update_dict = patient_update.model_dump(exclude_unset=True)

# Now only has fields that client actually sent!
# Example: {"city": "Mumbai", "weight": 90}
# NOT: {"name": None, "city": "Mumbai", "age": None, ...}
```

**Why?** Prevents overwriting with `None` values.

---

## DELETE Endpoint Architecture

### Simple Flow

```
1. Receive patient_id (path parameter)
   ↓
2. Load all patients from database
   ↓
3. Check if patient_id exists (→ 404 if not)
   ↓
4. Delete the patient record
   ↓
5. Save to database
   ↓
6. Return 200 OK response
```

### Python Dictionary Deletion

```python
# Delete key from dictionary
del data[patient_id]

# Save updated dictionary
save_patients_data(data)
```

---

## HTTP Status Codes

### 200 OK
- Update successful
- Delete successful
- General "operation completed"

### 204 No Content
- Alternative for successful delete
- No response body needed
- Rarely used

### 404 Not Found
- Patient doesn't exist
- Can't update/delete non-existent resource

---

## Common Patterns

### Pattern 1: Partial Update

```python
# Only send changed fields
{
  "weight": 90
}

# Server keeps other fields unchanged:
{
  "name": "John",        # unchanged
  "city": "Mumbai",      # CHANGED
  "weight": 90,          # CHANGED
  "age": 30,             # unchanged
  ...
}
```

### Pattern 2: Full Update

```python
# Send all fields for complete replacement
{
  "name": "John",
  "city": "Mumbai",
  "age": 30,
  "gender": "Male",
  "height": 1.78,
  "weight": 90
}
```

### Pattern 3: Validation on Update

```python
# Even if only age is sent, validation still applies
{
  "age": -5  # ← Invalid! Server returns validation error
}
```

---

## Interview Questions

**Q1: What's the difference between PUT and POST?**
A: POST creates new resources, PUT updates existing ones.

**Q2: Can you send partial data in PUT request?**
A: Yes! Using `Optional` fields and `exclude_unset=True`.

**Q3: What status code for successful update?**
A: 200 OK (not 201 Created, which is for POST only).

**Q4: What happens when you update weight?**
A: BMI and verdict are automatically recalculated (computed fields).

**Q5: How do you prevent `None` values from overwriting?**
A: Use `exclude_unset=True` when converting to dict.

**Q6: What status code when deleting non-existent patient?**
A: 404 Not Found.

**Q7: Can you update only one field?**
A: Yes, send only that field in request body.

**Q8: Is DELETE operation idempotent?**
A: First delete succeeds (200), second delete fails (404).

**Q9: How do you delete a record?**
A: `del data[patient_id]` then save.

**Q10: Why recalculate computed fields?**
A: To ensure BMI/verdict match new weight/height values.

---

## Idempotency

### GET - Idempotent
```
First GET: Returns patient → 200
Second GET: Returns patient → 200
No state changed
```

### POST - NOT Idempotent
```
First POST: Creates patient → 201
Second POST: Creates ANOTHER patient → 201
(Two patients created!)
```

### PUT - Idempotent
```
First PUT: Updates to city=Mumbai → 200
Second PUT: Updates to city=Mumbai → 200
Same result
```

### DELETE - NOT Idempotent (sort of)
```
First DELETE: Removes patient → 200
Second DELETE: Patient doesn't exist → 404
Different result!
```

---

## Complete CRUD Endpoints

```python
# CREATE
POST /create
Request Body: {new patient data}
Response: 201 Created

# READ (all)
GET /patients
Response: 200 OK + all patients

# READ (one)
GET /patients/{patient_id}
Response: 200 OK + one patient

# UPDATE
PUT /patients/{patient_id}
Request Body: {updated fields}
Response: 200 OK

# DELETE
DELETE /patients/{patient_id}
Response: 200 OK
```

---

## Next Chapter (6)

Will cover:
- Serving ML models with FastAPI
- Making predictions via API
- Real-world ML integration

👉 Start with `main.py` to see complete working code!
