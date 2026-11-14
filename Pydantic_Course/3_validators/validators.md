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

## 🤔 Confusing Questions (Follow-Up Interview Questions)

### Q11: If you have `@field_validator('age', mode='before')`, can you access the age field's type?

**Answer:**

YES! In 'before' mode, you get raw value before type conversion:

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    age: int

    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, v):
        # v might be a string "30" or int 30
        if isinstance(v, str) and not v.isdigit():
            raise ValueError("Age must be numeric string")
        return v

# ✅ Works: age="30" (string of digits)
user = User(age="30")

# ❌ Fails: age="abc" (non-numeric string)
user = User(age="abc")
```

---

### Q12: What's the difference between returning and raising in a validator?

**Answer:**

- **Return:** Use the returned value
- **Raise:** Validation fails with error

```python
class User(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        # ✅ Correct: transform and return
        return v.upper()

user = User(name="john")
print(user.name)  # "JOHN" (transformed!)

class User(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        # ❌ Also correct: reject invalid input
        if v == "admin":
            raise ValueError("Cannot use 'admin' as name")
        return v

user = User(name="admin")  # ❌ Fails
user = User(name="john")  # ✅ Works
```

---

### Q13: Can you call other validators from inside a validator?

**Answer:**

NO directly! Validators don't call each other. Use helpers:

```python
class User(BaseModel):
    email: str
    backup_email: str

    # ❌ Can't call validator from validator
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        # Can't call validate_backup_email() here
        return v

    # ✅ Use a helper function instead
    @classmethod
    def _is_valid_email(cls, email):
        return "@" in email and "." in email

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not cls._is_valid_email(v):
            raise ValueError("Invalid email")
        return v

    @field_validator('backup_email')
    @classmethod
    def validate_backup_email(cls, v):
        if not cls._is_valid_email(v):
            raise ValueError("Invalid backup email")
        return v
```

---

### Q14: If a validator returns None, does the field become None?

**Answer:**

YES! Returning None sets field to None:

```python
class User(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v == "":
            return None  # ← Setting to None
        return v

user = User(name="")
print(user.name)  # None (not empty string!)
```

**But be careful:** If field is NOT Optional, this might cause errors!

---

### Q15: Can you have multiple validators for the same field?

**Answer:**

YES! They run in order:

```python
class User(BaseModel):
    age: int

    @field_validator('age')
    @classmethod
    def age_positive(cls, v):
        if v < 0:
            raise ValueError("Age must be positive")
        return v

    @field_validator('age')
    @classmethod
    def age_reasonable(cls, v):
        if v > 150:
            raise ValueError("Age seems unrealistic")
        return v

# Both validators run in sequence
user = User(age=200)  # ❌ Fails second validator
user = User(age=30)  # ✅ Passes both
```

---

### Q16: What does `mode='wrap'` do?

**Answer:**

Wraps the validation, calling the default validator:

```python
from pydantic import field_validator

class User(BaseModel):
    age: int

    @field_validator('age', mode='wrap')
    @classmethod
    def validate_age(cls, v, handler):
        # handler = default Pydantic validator
        result = handler(v)  # Run default validation
        print(f"Age validated as: {result}")
        return result

user = User(age="30")  # "30" converts to 30 via handler
# Prints: Age validated as: 30
```

---

### Q17: If you use `@model_validator(mode='after')`, when does it run?

**Answer:**

AFTER all fields are validated individually:

```python
class User(BaseModel):
    password: str
    password_confirm: str

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("Passwords don't match")
        return self

# All field validators run first, THEN model validator
user = User(password="123", password_confirm="123")  # ✅ Works
user = User(password="123", password_confirm="456")  # ❌ Model validator fails
```

---

### Q18: Can a @model_validator modify multiple fields?

**Answer:**

YES! You can modify `self`:

```python
class User(BaseModel):
    first_name: str
    last_name: str
    full_name: str = ""

    @model_validator(mode='after')
    def set_full_name(self):
        self.full_name = f"{self.first_name} {self.last_name}"
        return self

user = User(first_name="John", last_name="Doe", full_name="")
print(user.full_name)  # "John Doe" (auto-set!)
```

---

### Q19: What happens if a field validator has an error that's also caught by model_validator?

**Answer:**

Field validator error is raised FIRST. Model validator never runs:

```python
class User(BaseModel):
    age: int

    @field_validator('age')
    @classmethod
    def validate_age_positive(cls, v):
        if v < 0:
            raise ValueError("Age must be positive")  # ← Raised first
        return v

    @model_validator(mode='after')
    def validate_model(self):
        if self.age > 150:
            raise ValueError("Age unrealistic")
        return self

user = User(age=-5)  # ❌ Field validator fails FIRST
user = User(age=200)  # ❌ Model validator fails (field passed)
```

---

### Q20: How do you write a validator that depends on another field's value?

**Answer:**

Use `@model_validator` to access other fields:

```python
class Order(BaseModel):
    order_type: str
    discount_code: Optional[str] = None

    @model_validator(mode='after')
    def validate_discount_code(self):
        # ✅ Can access any field
        if self.order_type == "regular" and self.discount_code:
            raise ValueError("Regular orders can't use discounts")
        if self.order_type == "premium" and not self.discount_code:
            raise ValueError("Premium orders require discount code")
        return self

# ✅ Works: regular without discount
order = Order(order_type="regular")

# ❌ Fails: regular with discount
order = Order(order_type="regular", discount_code="SAVE10")

# ❌ Fails: premium without discount
order = Order(order_type="premium")

# ✅ Works: premium with discount
order = Order(order_type="premium", discount_code="SAVE10")
```

---

## Next Steps

You now know how to build **custom validation logic**.

**Next Module (4_advanced)** will teach you:
- Nested models (composition)
- Computed fields
- Model export (to dict/JSON)

👉 Go to `4_advanced/advanced.md`
