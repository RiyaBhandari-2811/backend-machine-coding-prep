# Module 2: Data Validation with Field

## Overview

**Field()** is Pydantic's function to add validation constraints and metadata to model fields.

**Use Field() when you need to:**
- Add validation constraints (min, max, length)
- Add descriptions and examples (for docs)
- Set default values
- Enforce specific rules

---

## Field() Basics

### Syntax

```python
from pydantic import BaseModel, Field

class Patient(BaseModel):
    name: str = Field(
        ...,                    # ... means required
        description="Patient name",
        min_length=1,
        max_length=100
    )
    age: int = Field(
        ...,
        description="Patient age",
        gt=0,                   # greater than
        le=120                  # less than or equal
    )
```

### Field() Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `description` | Documentation | `description="Age in years"` |
| `example` | Example value | `example=30` |
| `title` | Display name | `title="Patient Age"` |
| `gt` | Greater than | `gt=0` |
| `ge` | Greater than or equal | `ge=0` |
| `lt` | Less than | `lt=150` |
| `le` | Less than or equal | `le=120` |
| `min_length` | Min string length | `min_length=3` |
| `max_length` | Max string length | `max_length=50` |

---

## Numeric Constraints

### Single Constraint

```python
class Patient(BaseModel):
    age: int = Field(gt=0)  # Must be > 0
```

### Range Constraint

```python
class Patient(BaseModel):
    age: int = Field(gt=0, le=120)  # 0 < age ≤ 120
```

---

## String Constraints

### Length Constraints

```python
class Patient(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8)  # At least 8 chars
```

### Regex Validation

```python
class Patient(BaseModel):
    patient_id: str = Field(
        pattern="^P[0-9]{3}$"  # P001, P002, etc.
    )
```

---

## List Constraints

### List Length

```python
from typing import List

class Patient(BaseModel):
    allergies: List[str] = Field(
        max_length=5  # Max 5 allergies
    )
```

---

## Required vs Optional

### Required (Default)

```python
class Patient(BaseModel):
    name: str  # Must provide this
```

### Optional with Default

```python
class Patient(BaseModel):
    nickname: Optional[str] = Field(None, description="Optional nickname")
```

### Optional with Custom Default

```python
class Patient(BaseModel):
    is_active: bool = Field(True, description="Patient active status")
```

---

## Adding Metadata

### For Documentation

```python
class Patient(BaseModel):
    name: str = Field(
        ...,
        title="Full Name",
        description="Patient's full legal name",
        examples=["John Smith", "Alice Johnson"]
    )
```

### Use Case: API Documentation

When using Pydantic with FastAPI, this metadata appears in auto-generated docs (Swagger UI).

---

## Common Patterns

### Pattern 1: Email Validation

```python
from pydantic import EmailStr

class User(BaseModel):
    email: EmailStr  # Automatically validates email format
```

### Pattern 2: Age Validation

```python
class Patient(BaseModel):
    age: int = Field(
        ...,
        ge=0,           # Age can't be negative
        le=150          # Reasonable upper limit
    )
```

### Pattern 3: Optional with Constraint

```python
from typing import Optional

class Patient(BaseModel):
    weight: Optional[float] = Field(None, gt=0)  # If provided, must be > 0
```

---

## Type Coercion

Pydantic automatically converts compatible types:

```python
class Order(BaseModel):
    quantity: int = Field(...)

# This works - "10" is converted to 10
order = Order(quantity="10")

# This fails - "abc" can't be converted to int
order = Order(quantity="abc")  # ValidationError!
```

### Strict Mode (No Coercion)

```python
class Order(BaseModel):
    quantity: int = Field(..., strict=True)

# This fails - no type coercion allowed
order = Order(quantity="10")  # ValidationError!

# This works - already correct type
order = Order(quantity=10)  # Success
```

---

## Computed Fields

Fields that are calculated from other fields:

```python
from pydantic import computed_field

class Rectangle(BaseModel):
    width: float
    height: float
    
    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height

rect = Rectangle(width=5, height=3)
print(rect.area)  # 15.0
```

---

## Interview Questions

**Q1: What's the difference between required and optional fields?**
A: Required fields must be provided. Optional fields can be None and need a default value.

**Q2: How do you validate a number is between 0 and 100?**
A: Use `Field(ge=0, le=100)` where ge=greater-than-equal, le=less-than-equal.

**Q3: What does `...` mean in Field()?**
A: It means the field is required. Same as Python's Ellipsis object.

**Q4: Can Pydantic convert "123" (string) to 123 (int)?**
A: Yes, by default. Use `strict=True` in Field() to disable this.

**Q5: How do you limit string length?**
A: Use `Field(min_length=1, max_length=50)`.

---

## Next Steps

You now know how to add **validation constraints** to your models.

**Next Module (3_validators)** will teach you:
- Field validators (custom validation per field)
- Model validators (validation across multiple fields)
- Before/After validation modes

👉 Go to `3_validators/validators.md`
