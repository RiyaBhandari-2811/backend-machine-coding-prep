# Module 4: Advanced Features

## Overview

Advanced Pydantic features for production applications:
- Nested models (composition)
- Computed fields
- Model export (dict/JSON)
- Complex configurations

---

## Nested Models

### What Are Nested Models?

Models containing other Pydantic models as fields.

### Simple Nesting

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str

class Patient(BaseModel):
    name: str
    address: Address  # Nested model
```

### Using Nested Models

```python
data = {
    "name": "John",
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "country": "USA"
    }
}

patient = Patient(**data)
print(patient.name)              # "John"
print(patient.address.street)    # "123 Main St"
print(patient.address.city)      # "New York"
```

### Benefits

- **Validation** - Each nested model is validated
- **Organization** - Better code structure
- **Reusability** - Address model can be used in Patient, Employee, etc.
- **Type Safety** - Clear types for nested data

---

## Computed Fields

### What Are Computed Fields?

Fields calculated from other fields using `@computed_field` decorator.

### Simple Computed Field

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float
    
    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height
```

### Using Computed Fields

```python
rect = Rectangle(width=5, height=3)
print(rect.area)  # 15.0

# Works in dict export too!
print(rect.model_dump())
# {'width': 5, 'height': 3, 'area': 15.0}
```

### When to Use

- Derived values (area, total, discount)
- Status flags (is_active, is_overdue)
- Formatted fields (full_name = first_name + last_name)

---

## Model Export

### Export to Dictionary

```python
patient = Patient(name="John", age=30, email="john@example.com")

# Convert to dict
patient_dict = patient.model_dump()
# {'name': 'John', 'age': 30, 'email': 'john@example.com'}

# Nested models also converted
patient_dict = patient_with_address.model_dump()
# {'name': 'John', 'address': {'street': '123 Main', ...}}
```

### Export to JSON String

```python
# Convert to JSON string
patient_json = patient.model_dump_json()
# '{"name":"John","age":30,"email":"john@example.com"}'

# Pretty JSON
patient_json = patient.model_dump_json(indent=2)
```

### Partial Export (Include/Exclude)

```python
# Only include specific fields
patient.model_dump(include={'name', 'age'})
# {'name': 'John', 'age': 30}

# Exclude specific fields
patient.model_dump(exclude={'email'})
# {'name': 'John', 'age': 30}

# Exclude unset fields
patient.model_dump(exclude_unset=True)
```

---

## Model Configuration

### Config Class

```python
class Patient(BaseModel):
    name: str
    age: int
    
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Strip whitespace
        validate_assignment=True,    # Validate on assignment
        use_enum_values=True,        # Use enum values, not names
    )
```

---

## Common Patterns

### Pattern 1: Nested Patient with Address

```python
class Address(BaseModel):
    street: str
    city: str
    zipcode: str

class Patient(BaseModel):
    name: str
    age: int
    address: Address

# Validate nested structure
data = {
    "name": "John",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "Boston",
        "zipcode": "02101"
    }
}
patient = Patient(**data)
```

### Pattern 2: Computed Medical Metrics

```python
from pydantic import computed_field

class Patient(BaseModel):
    name: str
    weight_kg: float  # in kilograms
    height_m: float   # in meters
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight_kg / (self.height_m ** 2)
    
    @computed_field
    @property
    def bmi_category(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"
```

### Pattern 3: API Response Serialization

```python
class PatientResponse(BaseModel):
    id: int
    name: str
    email: str
    
    def to_dict(self):
        return self.model_dump()
    
    def to_json(self):
        return self.model_dump_json()

# Use in FastAPI
# @app.get("/patients/{id}")
# def get_patient(id: int):
#     patient = database.get_patient(id)
#     return PatientResponse(**patient).model_dump()
```

---

## Interview Questions

**Q1: What's the difference between nested models and inheritance?**
A: Nested models (composition) contain other models as fields. Inheritance means one model inherits from another.

**Q2: When should you use @computed_field?**
A: When you need a field calculated from other fields (area, status, full_name).

**Q3: How do you exclude fields when exporting?**
A: Use `model.model_dump(exclude={'field1', 'field2'})`.

**Q4: Can computed fields appear in model_dump()?**
A: Yes! Computed fields are included by default in model_dump().

**Q5: What's the difference between model_dump() and model_dump_json()?**
A: model_dump() returns a Python dict. model_dump_json() returns a JSON string.

---

## 🤔 Confusing Questions (Follow-Up Interview Questions)

### Q11: Can you have a @computed_field that depends on another @computed_field?

**Answer:**

YES! Computed fields can chain:

```python
from pydantic import BaseModel, computed_field

class User(BaseModel):
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @computed_field
    @property
    def full_name_uppercase(self) -> str:
        return self.full_name.upper()  # ← Uses another computed field!

user = User(first_name="john", last_name="doe")
print(user.full_name)  # "john doe"
print(user.full_name_uppercase)  # "JOHN DOE"
```

---

### Q12: If you exclude a field in model_dump(), can you still access it on the object?

**Answer:**

YES! Exclude only affects the dict export:

```python
class User(BaseModel):
    name: str
    password: str

user = User(name="john", password="secret123")

# Exclude password from dict
user_dict = user.model_dump(exclude={'password'})
print(user_dict)  # {'name': 'john'} (password missing)

# But object still has password!
print(user.password)  # "secret123" (still there!)
```

**This is important for security:** Always exclude sensitive fields when returning to clients.

---

### Q13: Can you use `exclude` with nested models?

**Answer:**

YES! Use dot notation:

```python
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    address: Address

user = User(
    name="john",
    address=Address(street="123 Main", city="NYC", zip_code="10001")
)

# Exclude nested field
user_dict = user.model_dump(exclude={'address': {'zip_code'}})
print(user_dict)
# {'name': 'john', 'address': {'street': '123 Main', 'city': 'NYC'}}
# zip_code excluded!
```

---

### Q14: What's the difference between `exclude` and `include` in model_dump()?

**Answer:**

- **exclude:** Remove fields from output
- **include:** Keep ONLY specified fields

```python
user = User(name="john", age=30, email="john@example.com", phone="555-1234")

# exclude: Remove these
dict1 = user.model_dump(exclude={'phone', 'email'})
# {'name': 'john', 'age': 30}

# include: Keep ONLY these
dict2 = user.model_dump(include={'name', 'age'})
# {'name': 'john', 'age': 30}

# Result is same, but approach is different!
```

---

### Q15: Can model_dump_json() fail if your model has non-JSON types?

**Answer:**

YES! Some Python objects aren't JSON serializable:

```python
from datetime import datetime

class Event(BaseModel):
    name: str
    date: datetime  # Pydantic handles this well

event = Event(name="Meeting", date=datetime.now())

# ✅ Works: Pydantic converts datetime to ISO string
json_str = event.model_dump_json()
print(json_str)  # {"name":"Meeting","date":"2024-01-15T10:30:00"}

# ❌ But custom objects fail:
class User(BaseModel):
    name: str
    file: open  # File object

user = User(name="john", file=open("test.txt"))
json_str = user.model_dump_json()  # ❌ TypeError! File not JSON serializable
```

---

### Q16: Can you have circular references in nested models?

**Answer:**

YES! Using `from __future__ import annotations`:

```python
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    friends: Optional[list[User]] = None  # ← Refers to itself!

user_dict = {
    "name": "John",
    "friends": [
        {"name": "Alice", "friends": None},
        {"name": "Bob", "friends": None}
    ]
}

user = User(**user_dict)
print(user.friends[0].name)  # "Alice"
```

---

### Q17: What happens if you call model_dump_json() on a very large model?

**Answer:**

It's generally fine, but watch performance:

```python
# Large nested model with thousands of items
big_model = LargeModel(items=[...]*10000)

# Converts all to JSON (might be slow)
json_str = big_model.model_dump_json()
print(len(json_str))  # Very large string!

# Alternative: Use streaming or pagination
# Don't dump huge models at once
```

---

### Q18: Can you customize how model_dump_json() formats output?

**Answer:**

YES! Using `by_alias`, `indent`, etc:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(alias="full_name")
    age: int

user = User(full_name="John", age=30)

# Use aliases in JSON
json1 = user.model_dump_json(by_alias=True)
print(json1)  # {"full_name":"John","age":30}

# Pretty print
json2 = user.model_dump_json(indent=2)
print(json2)
# {
#   "name": "John",
#   "age": 30
# }
```

---

### Q19: If you inherit from a Pydantic model, can you override fields?

**Answer:**

YES, but with caveats:

```python
class User(BaseModel):
    name: str
    age: int

class Admin(User):
    role: str = "admin"
    # age is inherited

admin = Admin(name="John", age=30)  # ✅ Works

# But be careful with validation:
class Admin(User):
    age: int = 18  # Override with default

admin1 = Admin(name="John")  # age defaults to 18
admin2 = Admin(name="John", age=50)  # age is 50
```

---

### Q20: Can you use computed_field with parameters?

**Answer:**

NO! Computed fields take no parameters:

```python
class User(BaseModel):
    price: float

    # ❌ WRONG - Can't accept parameters
    @computed_field
    @property
    def discount_price(self, percentage) -> float:  # ← No!
        return self.price * (1 - percentage)

    # ✅ CORRECT - Use default logic
    @computed_field
    @property
    def discount_price(self) -> float:
        return self.price * 0.9  # Always 10% discount

user = User(price=100)
print(user.discount_price)  # 90 (always 10% off)
```

---

## Use Cases

### Use Case 1: FastAPI Response Models

```python
class PatientResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        # Configure for API response

@app.get("/patients/{id}", response_model=PatientResponse)
def get_patient(id: int):
    pass
```

### Use Case 2: Database Models

```python
class PatientDB(BaseModel):
    id: int
    name: str
    created_at: datetime
```

### Use Case 3: Configuration Management

```python
class AppConfig(BaseModel):
    database_url: str
    debug: bool = False
    max_connections: int = 10
```

### Use Case 4: ML Model Input Validation

```python
class PredictionInput(BaseModel):
    age: int
    weight: float
    height: float
    has_diabetes: bool
```

---

## Next Steps

You've completed the **entire Pydantic course**!

### What You Learned

✅ **Module 1: Basics** - Why Pydantic, BaseModel, type hints  
✅ **Module 2: Validation** - Field constraints, data validation  
✅ **Module 3: Validators** - Custom validation logic  
✅ **Module 4: Advanced** - Nested models, computed fields, export  

### Real-World Applications

**FastAPI** - Build type-safe APIs  
**Configuration Management** - Load and validate config files  
**Data Pipelines** - Validate data at each stage  
**ML Systems** - Validate model inputs/outputs  

### Practice Exercises

1. Create nested Patient model with Address and Insurance
2. Add computed field for patient BMI
3. Export patient to JSON for API response
4. Add email/phone validators
5. Implement model_dump with include/exclude

---

## Resources

- **Pydantic Docs** - https://docs.pydantic.dev/
- **FastAPI Integration** - Works seamlessly with FastAPI
- **Type Hints** - Python typing documentation

**Congratulations! You're now a Pydantic expert! 🎉**
