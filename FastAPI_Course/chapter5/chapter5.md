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

## 🤔 Confusing Questions (Follow-Up Interview Questions)

### Q11: What if you send `exclude_unset=False` instead of `exclude_unset=True` in a PUT update?

**Answer:**

It changes which fields get updated:

```python
class PatientUpdate(BaseModel):
    weight: Optional[float] = None
    height: Optional[float] = None

# Client sends: {"weight": 90}

# With exclude_unset=False (WRONG):
update_dict = patient_update.model_dump(exclude_unset=False)
# Result: {"weight": 90, "height": None}  ← Height becomes None!
# Problem: Overwrites height with None even though client didn't send it!

# With exclude_unset=True (CORRECT):
update_dict = patient_update.model_dump(exclude_unset=True)
# Result: {"weight": 90}  ← Only sent fields included
# Good: Height is NOT overwritten!
```

**The difference:**

- `exclude_unset=True` → Only fields client actually sent
- `exclude_unset=False` → ALL fields (None values included)

**Always use `exclude_unset=True` for partial updates!**

---

### Q12: What's the difference between PUT and PATCH? When do you use each?

**Answer:**

| Aspect | PUT | PATCH |
|--------|-----|-------|
| **Purpose** | Full update | Partial update |
| **Required** | All fields | Only changed fields |
| **Missing fields** | Cleared/reset | Unchanged |
| **Idempotent** | YES | YES (usually) |
| **Use case** | Replace entire resource | Modify specific fields |

**Examples:**

```python
# Original patient
{
  "name": "John",
  "age": 30,
  "city": "Mumbai",
  "weight": 75
}

# PUT request (full update - must send ALL fields)
PUT /patients/P001
{
  "name": "John",
  "age": 31,
  "city": "Delhi",      # ← REQUIRED in PUT
  "weight": 75          # ← REQUIRED in PUT
}
# Result: All fields updated as sent

# PATCH request (partial update - send only changed)
PATCH /patients/P001
{
  "age": 31,
  "city": "Delhi"
}
# Result: Only age and city updated, name/weight unchanged
```

**But FastAPI convention:**
- Most use PUT for both full and partial
- PATCH is less common in practice

---

### Q13: Can you DELETE a patient and then POST with the same patient_id? What happens?

**Answer:**

YES! You can reuse the ID after deletion:

```python
# Step 1: Delete patient P001
DELETE /patients/P001
# Response: 200 OK, patient P001 is removed

# Step 2: Create new patient P001
POST /patients
{
  "patient_id": "P001",
  "name": "Different John",
  ...
}
# Response: 201 Created, new patient P001 created
# It's a DIFFERENT person with same ID!
```

**This can be dangerous!** Consider:

```python
# Step 1: Delete John's data
DELETE /patients/P001

# Step 2: Much later, create patient P001 (different person)
POST /patients with P001
# Now P001 is a different person!

# Step 3: Old code trying to access John's data
GET /patients/P001
# Returns different person's data! (data leak!)
```

**Solutions:**

1. **Use UUIDs** (hard to guess/reuse)
```python
patient_id: str = str(uuid.uuid4())
# Can't predict or reuse
```

2. **Auto-increment** (used by our current system)
```python
# P001, P002, P003... can't skip back
```

3. **Soft delete** (mark deleted, don't remove)
```python
class Patient(BaseModel):
    deleted: bool = False

# DELETE marks as deleted, doesn't remove
# GET returns 404 for deleted patients
```

---

### Q14: What if a PUT request provides all fields, but one field has validation error?

**Answer:**

FastAPI returns 422 validation error **BEFORE** updating anything:

```python
class Patient(BaseModel):
    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    age: int = Field(..., ge=0, le=150)

# Original patient
{"weight": 75, "height": 1.8, "age": 30}

# PUT request with invalid age
PUT /patients/P001
{
  "weight": 75,
  "height": 1.8,
  "age": -5  # ← INVALID!
}

# Response: 422 Unprocessable Entity
# Database NOT updated! Transaction is atomic.
```

**This is great for data integrity!** Either all fields update, or none.

**But watch out for this pattern:**

```python
# If you manually extract and update:
data[patient_id]['weight'] = 75
data[patient_id]['height'] = 1.8
data[patient_id]['age'] = -5  # ← Bug! No validation!

# You bypass validation! age becomes -5!
# Always use Pydantic models for updates!
```

---

### Q15: Can you DELETE all patients at once? Can a single DELETE endpoint remove multiple records?

**Answer:**

Standard REST DELETE removes ONE resource:

```python
# DELETE single patient
DELETE /patients/P001
# Removes only P001

# DELETE all patients (not standard)
DELETE /patients
# Removes all? Not REST compliant!
```

**Standard way to DELETE multiple:**

```python
# Option 1: Multiple requests (ugly)
DELETE /patients/P001
DELETE /patients/P002
DELETE /patients/P003

# Option 2: Query parameter (non-standard but used)
DELETE /patients?ids=P001,P002,P003

# Option 3: POST with list of IDs (confusing method)
POST /patients/bulk-delete
{
  "patient_ids": ["P001", "P002", "P003"]
}
```

**Best practice:** If you need bulk deletes, clearly document it as non-standard:

```python
@app.delete("/patients/bulk-delete")
async def bulk_delete(patient_ids: List[str]):
    """
    Non-standard endpoint for bulk deletion.
    Use with caution!
    """
    for pid in patient_ids:
        if pid in data:
            del data[pid]
    return {"deleted": len(patient_ids)}
```

---

### Q16: What if a computed field depends on an updated field? Is it automatically recalculated?

**Answer:**

YES! When you create a Pydantic object, ALL computed fields recalculate:

```python
from pydantic import BaseModel, computed_field

class Patient(BaseModel):
    weight: float
    height: float
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

# Update logic
updated_data = {**existing_patient, **update_dict}
patient_obj = Patient(**updated_data)  # ← Creates new object
updated_dict = patient_obj.model_dump()

# BMI is automatically recalculated!
```

**But watch out:**

```python
# ❌ WRONG - Just update dict directly
data['P001']['weight'] = 90
# BMI is now STALE! Not recalculated!

# ✅ CORRECT - Recreate Pydantic object
patient_obj = Patient(**data['P001'])
patient_obj.weight = 90
updated_data = patient_obj.model_dump()
# BMI is fresh!
```

---

### Q17: Is a failed DELETE request still idempotent if it returns 404?

**Answer:**

This is philosophically tricky. Technically NO, but practically YES:

```python
# First DELETE
DELETE /patients/P001
# Response: 200 OK (deleted successfully)

# Second DELETE
DELETE /patients/P001
# Response: 404 Not Found (patient doesn't exist)

# Different status codes (200 vs 404) = technically NOT idempotent
# But the end result is the same: patient doesn't exist
```

**Idempotency definition varies:**

- **Strict**: Same status code always (200) = idempotent
- **Loose**: Same end state achieved (resource deleted) = idempotent

**Best practice:** Return 404 for second DELETE, it's clearer:

```python
@app.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int):
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Not found")
    del data[patient_id]
    return {"message": "Deleted"}
```

**Or make it idempotent (always 200):**

```python
@app.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int):
    if patient_id in data:
        del data[patient_id]
    return {"message": "Deleted"}  # 200 even if not found
```

---

### Q18: Can you use PUT to create a resource if it doesn't exist? Or must POST always be used?

**Answer:**

Technically PUT CAN create, and some APIs do this (called "PUT-based creation"):

```python
# Standard way (POST creates)
POST /patients
{"patient_id": "P001", "name": "John"}
# Response: 201 Created

# Alternative way (PUT creates if not exists)
PUT /patients/P001
{"name": "John"}
# Response: 201 Created (if new) or 200 OK (if update)
```

**This is rare and not REST compliant!** The standard says:

- **POST** creates new resources
- **PUT** updates existing resources

**Problems with PUT-based creation:**

```python
# Ambiguous response: 201 or 200?
# Client doesn't know if resource was created or updated
# Harder to implement
# Breaks REST conventions
```

**Stick with standard:**

```python
# POST for creation
POST /patients

# PUT for update
PUT /patients/P001
```

---

### Q19: What happens if you update a computed field dependency? Does the dependent field update automatically?

**Answer:**

YES, if you recreate the Pydantic object:

```python
class Patient(BaseModel):
    weight: float
    height: float
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    @computed_field
    @property
    def bmi_category(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        else:
            return "Overweight"

# Update weight
update_data = {"weight": 85}

# Recreate object (all computed fields recalculate!)
patient_obj = Patient(**{**existing_data, **update_data})

# Now both BMI and BMI_CATEGORY are fresh!
result = patient_obj.model_dump()
# bmi: 26.3
# bmi_category: "Overweight" (automatically updated!)
```

**Chain of updates:**
```
weight changed
  ↓
bmi recalculated
  ↓
bmi_category recalculated (depends on bmi!)
```

---

### Q20: Can you have a conditional PUT that only updates if certain conditions are met?

**Answer:**

YES! Common pattern called "conditional updates":

```python
@app.put("/patients/{patient_id}")
async def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    if_version: int = Header(None)  # Optimistic locking
):
    if patient_id not in data:
        raise HTTPException(404, "Not found")
    
    # Conditional check
    if if_version and data[patient_id]['version'] != if_version:
        raise HTTPException(409, "Resource changed, update failed")
    
    # Update
    data[patient_id].update(patient_update.dict(exclude_unset=True))
    data[patient_id]['version'] += 1
    
    return data[patient_id]

# Usage:
# PUT /patients/P001
# Headers: If-Version: 3
# Body: {"weight": 85}
# If version matches, update succeeds
# If version changed, returns 409 Conflict
```

**Use cases:**

- **Optimistic locking** - Detect concurrent modifications
- **Conditional updates** - "Only update if price hasn't changed"
- **Race condition prevention** - Prevent lost updates

**Status codes:**
- **200 OK** - Update succeeded
- **409 Conflict** - Condition failed, update rejected

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
