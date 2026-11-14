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

## Interview Questions

**Q1: What's the main purpose of Pydantic?**
A: Validate and parse data automatically, convert types, and catch errors early.

**Q2: Why use Pydantic instead of regular Python classes?**
A: Type checking, automatic conversion, validation, and clear error messages.

**Q3: What happens if you pass the wrong type to a Pydantic model?**
A: It tries to convert it. If conversion fails, raises ValidationError.

**Q4: Can you modify a Pydantic object after creation?**
A: By default NO (immutable). But you can use `model_config` to allow it.

**Q5: What does `model_dump()` return?**
A: A Python dictionary with all model fields and values.

**Q6: What does `model_dump_json()` return?**
A: A JSON string representation of the model.

**Q7: How do you access a field from a Pydantic model?**
A: Use dot notation: `model.field_name`

**Q8: What's the difference between `BaseModel` and a regular class?**
A: BaseModel adds validation, type checking, and serialization capabilities.

**Q9: Can Pydantic convert strings to numbers?**
A: Yes! `"123"` converts to `123`, but `"abc"` doesn't convert to int.

**Q10: What happens if a required field is missing?**
A: ValidationError is raised with details about which field is missing.

---

## 🤔 Confusing Questions (Follow-Up Interview Questions)

### Q11: If you define a model with `name: str`, can you pass `name=None`?

**Answer:**

NO! `None` is rejected for required fields:

```python
class User(BaseModel):
    name: str  # Required, non-optional

# ❌ This FAILS
user = User(name=None)
# ValidationError: Input should be a valid string

# ✅ This WORKS
user = User(name="John")

# To allow None, use Optional:
class User(BaseModel):
    name: Optional[str] = None  # Now None is allowed
    
user = User(name=None)  # ✅ Works
```

---

### Q12: What's the difference between `name: str = None` and `name: Optional[str] = None`?

**Answer:**

They look similar but have DIFFERENT meanings:

```python
# ❌ WRONG - This will fail!
class User(BaseModel):
    name: str = None
# ValidationError: name=None is invalid (str doesn't accept None)

# ✅ CORRECT - This works
class User(BaseModel):
    name: Optional[str] = None
# Optional[str] explicitly allows str OR None
```

**Why the difference:**

```
str = "only strings allowed"
Optional[str] = "strings OR None allowed"
```

---

### Q13: Can you create a Pydantic model without any fields?

**Answer:**

YES, but it's unusual:

```python
# Empty model
class Empty(BaseModel):
    pass

obj = Empty()  # ✅ Works, empty object
print(obj.model_dump())  # {}
```

**But it's useless!** Why would you want an empty model?

---

### Q14: If model_dump() returns a dict, can you modify it and the model stays the same?

**Answer:**

YES! Changes to the dict don't affect the model (they're separate objects):

```python
user = User(name="John", age=30)

user_dict = user.model_dump()
user_dict["name"] = "Alice"  # Modify dict

print(user.name)  # "John" (unchanged)
print(user_dict["name"])  # "Alice" (changed)
```

**This is key:** `model_dump()` creates a COPY, not a reference.

---

### Q15: Can you pass extra fields that aren't defined in the model?

**Answer:**

NO by default! Extra fields are ignored:

```python
class User(BaseModel):
    name: str
    age: int

# Extra fields (city) are IGNORED
user = User(name="John", age=30, city="Mumbai")
print(user.model_dump())
# {'name': 'John', 'age': 30}
# city is gone!
```

**To allow extra fields:**

```python
class User(BaseModel):
    model_config = ConfigDict(extra='allow')
    name: str
    age: int

user = User(name="John", age=30, city="Mumbai")
print(user.model_dump())
# {'name': 'John', 'age': 30, 'city': 'Mumbai'}
# city is included!
```

---

### Q16: What happens if you create a model instance but don't provide all required fields?

**Answer:**

ValidationError is raised immediately:

```python
class User(BaseModel):
    name: str
    age: int
    email: str

# Missing email!
user = User(name="John", age=30)
# ValidationError: 1 validation error for User
# email - Field required
```

---

### Q17: Can you use type hints like `List[str]` in Pydantic models?

**Answer:**

YES! Pydantic supports complex types:

```python
from typing import List, Dict, Optional

class User(BaseModel):
    name: str
    tags: List[str]  # List of strings
    metadata: Dict[str, int]  # Dictionary
    phone: Optional[str] = None  # Optional

user = User(
    name="John",
    tags=["python", "fastapi"],
    metadata={"age": 30, "score": 95},
    phone=None
)
print(user.tags)  # ['python', 'fastapi']
```

---

### Q18: If you call `model_dump_json()`, can you still access fields with dot notation?

**Answer:**

NO! `model_dump_json()` returns a STRING, not an object:

```python
user = User(name="John", age=30)

user_json = user.model_dump_json()
# '{"name":"John","age":30}'

# ❌ Can't use dot notation on string
print(user_json.name)  # AttributeError!

# ✅ Can still use original object
print(user.name)  # "John"

# ✅ Parse JSON string back to dict, then access
import json
data = json.loads(user_json)
print(data["name"])  # "John"
```

---

### Q19: What's the performance difference between `str` and `Optional[str]`?

**Answer:**

NO significant difference! Pydantic handles both efficiently.

```
str: Validates is string
Optional[str]: Validates is string OR None (slightly more checks)

Difference: Microseconds (negligible)
```

---

### Q20: Can you inherit from one Pydantic model to create another?

**Answer:**

YES! Pydantic supports inheritance:

```python
class Person(BaseModel):
    name: str
    age: int

class Employee(Person):
    employee_id: int
    salary: float

emp = Employee(name="John", age=30, employee_id=101, salary=50000)
print(emp.model_dump())
# {'name': 'John', 'age': 30, 'employee_id': 101, 'salary': 50000}

# Employee inherits name and age from Person!
```

---

## Next Steps

You now understand **why** Pydantic exists and **how** it works at a basic level.

**Next Module (2_validation)** will teach you:
- How to add validation constraints
- How to make fields required/optional
- How to use the Field() function

👉 Go to `2_validation/validation.md`
