# Module 1: Pydantic Basics

## What is Pydantic?

**Definition:** Pydantic is a Python library that uses type hints to perform data validation and settings management.

**Key Characteristics:**
- Uses Python type annotations
- Automatic data validation
- Clear error messages
- Supports complex data types
- Production-ready

## Why We Need Pydantic

### Problem 1: Type Validation in Python

Python is **dynamically typed** - you can assign any type to a variable:

```python
# Without validation - DANGEROUS
def insert_patient(name, age):
    print(f"Inserting: {name}, {age}")

# This works (but shouldn't!)
insert_patient("John", "thirty")  # age should be int, not string!
```

**Issue:** Python allows wrong data types. Only developers catch this.

### Problem 2: No Built-in Data Constraints

No automatic validation of data rules:

```python
# Without validation
def insert_patient(name, age):
    # Age should never be negative!
    print(f"Inserting: {name}, {age}")

insert_patient("John", -5)  # Accepted! But invalid!
```

**Solution:** Pydantic solves both problems automatically.

---

## How Pydantic Works

**3 Steps:**

1. **Define Schema** - Create a Pydantic model with type hints
2. **Validate Data** - Create model instance from user input
3. **Use Validated Data** - Your data is guaranteed to be correct

### Step 1: Define Schema

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name: str      # Must be string
    age: int       # Must be integer
```

### Step 2: Validate Data

```python
# User provides data
user_data = {"name": "John", "age": 30}

# Pydantic validates it
patient = Patient(**user_data)
# ✅ Success! Data is valid

# Invalid data
invalid_data = {"name": "John", "age": "thirty"}
patient = Patient(**invalid_data)
# ❌ ValidationError! age must be int
```

### Step 3: Use Data

```python
print(patient.name)  # "John"
print(patient.age)   # 30
# You know data is correct!
```

---

## Creating Your First Model

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int
    email: str

# Valid data - works
patient1 = Patient(
    name="Alice",
    age=28,
    email="alice@example.com"
)
print(patient1)
# name='Alice' age=28 email='alice@example.com'

# Invalid data - fails
patient2 = Patient(
    name="Bob",
    age="thirty",  # ❌ Wrong type!
    email="bob@example.com"
)
# ValidationError: age must be a valid integer
```

---

## Type Hints Overview

| Type | Example |
|------|---------|
| `str` | `"Hello"` |
| `int` | `42` |
| `float` | `3.14` |
| `bool` | `True` |
| `list` | `[1, 2, 3]` |
| `dict` | `{"key": "value"}` |

### Complex Types

```python
from typing import List, Dict, Optional

class Patient(BaseModel):
    name: str
    allergies: List[str]              # List of strings
    contacts: Dict[str, str]          # Dict with str keys/values
    emergency_phone: Optional[str]    # Optional (can be None)
```

---

## Key Concepts

### BaseModel
Every Pydantic model inherits from `BaseModel`. This gives your model:
- Data validation
- Type checking
- Useful methods (.dict(), .json(), etc.)

### Type Hints
Pydantic uses Python's type hints to:
- Document what types are expected
- Automatically validate incoming data
- Provide IDE autocomplete

### Automatic Validation
When you create a model instance, Pydantic:
1. Checks all required fields are present
2. Validates data types
3. Converts types when possible
4. Raises errors on invalid data

---

## Common Patterns

### Pattern 1: Simple Model

```python
class Book(BaseModel):
    title: str
    author: str
    pages: int
```

### Pattern 2: Model with Optional Fields

```python
class Book(BaseModel):
    title: str
    author: str
    pages: int
    isbn: Optional[str] = None  # Optional, defaults to None
```

### Pattern 3: Model with Default Values

```python
class Book(BaseModel):
    title: str
    author: str
    pages: int
    available: bool = True  # Default to True
```

---

## Next Steps

You now understand **why** Pydantic exists and **how** it works at a basic level.

**Next Module (2_validation)** will teach you:
- How to add validation constraints
- How to make fields required/optional
- How to use the Field() function

👉 Go to `2_validation/validation.md`
