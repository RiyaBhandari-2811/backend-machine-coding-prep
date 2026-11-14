# Module 3: Custom Validators

## Overview

**Validators** are custom functions that run additional validation logic beyond what Field() can do.

**Two types of validators:**
1. **@field_validator** - Validates a single field
2. **@model_validator** - Validates entire model or multiple fields together

---

## Field Validator Basics

### Simple Field Validator

```python
from pydantic import BaseModel, field_validator

class Patient(BaseModel):
    name: str
    age: int
    
    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        if len(v) < 3:
            raise ValueError('Name must be at least 3 characters')
        return v.title()  # Convert to title case
```

### How It Works

1. Decorator `@field_validator('name')` - Applies to 'name' field
2. Function receives field value `v`
3. Validate and optionally transform the value
4. Return transformed value or raise `ValueError`

---

## Validating Multiple Fields

### Single Validator for Multiple Fields

```python
class Patient(BaseModel):
    first_name: str
    last_name: str
    
    @field_validator('first_name', 'last_name')
    def validate_names(cls, v):
        if not v or not v.strip():
            raise ValueError('Names cannot be empty')
        return v.strip().title()
```

---

## Before/After Validation Mode

### After Mode (Default)

```python
@field_validator('age')
def validate_age(cls, v):
    # Runs AFTER Pydantic's type conversion
    # v is already an int
    if v < 0:
        raise ValueError('Age cannot be negative')
    return v
```

### Before Mode

```python
@field_validator('age', mode='before')
def validate_age(cls, v):
    # Runs BEFORE Pydantic's type conversion
    # v might be string "25" or int 25
    if isinstance(v, str):
        if not v.isdigit():
            raise ValueError('Age must be numeric')
    return v
```

### Use Cases

| Mode | When to Use |
|------|-------------|
| `after` (default) | Type is guaranteed correct, focus on value logic |
| `before` | Need to handle/transform raw input before type conversion |

---

## Model Validator

### Validate Across Multiple Fields

```python
from pydantic import model_validator

class DateRange(BaseModel):
    start_date: str
    end_date: str
    
    @model_validator(mode='after')
    def validate_dates(self):
        # self is the entire model instance
        if self.start_date >= self.end_date:
            raise ValueError('Start date must be before end date')
        return self
```

### When to Use Model Validator

- Validate relationships between fields
- Check one field against another
- Complex logic across multiple fields

---

## Common Validation Patterns

### Pattern 1: Email Domain Validation

```python
class User(BaseModel):
    email: str
    
    @field_validator('email')
    def validate_email_domain(cls, v):
        if not '@' in v:
            raise ValueError('Invalid email')
        domain = v.split('@')[1]
        allowed_domains = ['gmail.com', 'company.com']
        if domain not in allowed_domains:
            raise ValueError(f'Email domain {domain} not allowed')
        return v.lower()
```

### Pattern 2: Conditional Validation

```python
class Medication(BaseModel):
    name: str
    dose: Optional[str]
    requires_prescription: bool
    
    @model_validator(mode='after')
    def validate_prescription(self):
        if self.requires_prescription and not self.dose:
            raise ValueError('Prescription medications must have a dose')
        return self
```

### Pattern 3: Value Transformation

```python
class Patient(BaseModel):
    phone: str
    
    @field_validator('phone')
    def format_phone(cls, v):
        # Remove non-digits
        digits = ''.join(c for c in v if c.isdigit())
        if len(digits) != 10:
            raise ValueError('Phone must have 10 digits')
        # Transform to (XXX) XXX-XXXX format
        return f'({digits[:3]}) {digits[3:6]}-{digits[6:]}'
```

---

## Field Info Access

### Get Field Metadata

```python
from pydantic import field_validator

class Product(BaseModel):
    price: float
    
    @field_validator('price')
    def validate_price(cls, v, info):
        # info.field_name = 'price'
        # info.data = {'all_fields_validated_so_far': ...}
        if v < 0:
            raise ValueError(f'{info.field_name} cannot be negative')
        return v
```

---

## Error Messages

### Custom Error Message

```python
class Patient(BaseModel):
    age: int
    
    @field_validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Age must be between 0 and 150')
        return v
```

### Pydantic Shows Error

```
ValidationError: 1 validation error for Patient
age
  Age must be between 0 and 150 (type=value_error)
```

---

## Interview Questions

**Q1: What's the difference between @field_validator and @model_validator?**
A: @field_validator validates a single field. @model_validator validates the entire model or relationships between fields.

**Q2: When would you use mode='before' vs mode='after'?**
A: Use 'before' to handle raw input before type conversion. Use 'after' (default) when type is guaranteed.

**Q3: Can one validator handle multiple fields?**
A: Yes! Use `@field_validator('field1', 'field2')` to validate multiple fields with same logic.

**Q4: How do you transform a field value?**
A: Return the transformed value from the validator function. Example: return v.upper()

**Q5: When should you use @model_validator?**
A: When validating requires comparing two or more fields, or complex cross-field logic.

---

## Next Steps

You now know how to build **custom validation logic**.

**Next Module (4_advanced)** will teach you:
- Nested models (composition)
- Computed fields
- Model export (to dict/JSON)

👉 Go to `4_advanced/advanced.md`
