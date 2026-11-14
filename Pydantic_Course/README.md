# Pydantic Course - Complete Guide

**Pydantic** is a Python library for data validation and settings management using Python type annotations.

## Course Structure

This course is organized into **4 focused modules**:

### 📚 Module 1: Basics
**Location:** `1_basics/`

Learn why Pydantic is needed and how to create your first data models.

- What is Pydantic?
- Problems it solves (Type validation, Data validation)
- Creating BaseModel classes
- Type hints in Python

**Files:**
- `basics.md` - Concepts and explanations
- `main.py` - Practical examples

---

### ✅ Module 2: Validation
**Location:** `2_validation/`

Master type validation and data constraints using Field function.

- Type validation in Pydantic
- Using Field() for constraints
- Required vs Optional fields
- Common validation patterns

**Files:**
- `validation.md` - Validation techniques
- `main.py` - Practical validation examples

---

### 🔍 Module 3: Validators
**Location:** `3_validators/`

Build custom validation logic for fields and entire models.

- Field validators (@field_validator)
- Model validators (@model_validator)
- Before/After validation modes
- Cross-field validation

**Files:**
- `validators.md` - Custom validation patterns
- `main.py` - Validator examples

---

### 🚀 Module 4: Advanced
**Location:** `4_advanced/`

Advanced features: computed fields, nested models, and export.

- Computed fields (@computed_field)
- Nested models
- Model composition
- Exporting to dict/JSON

**Files:**
- `advanced.md` - Advanced concepts
- `main.py` - Advanced examples

---

## How to Use This Course

1. **Start with Module 1** - Understand the basics
2. **Move to Module 2** - Learn validation patterns
3. **Master Module 3** - Build custom validators
4. **Explore Module 4** - Advanced features

Each module is **self-contained** but builds on previous knowledge.

## Quick Start

```python
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int

# Create and validate
patient = Patient(name="John", age=30)
print(patient)  # name='John' age=30
```

---

## Interview Topics Covered

✅ Why Pydantic is needed  
✅ Type validation  
✅ Data validation  
✅ Field validators  
✅ Model validators  
✅ Computed fields  
✅ Nested models  
✅ Model export  

---

**Total Time to Complete:** ~2-3 hours  
**Difficulty:** Beginner to Intermediate  
**Prerequisites:** Python basics, type hints

Start with **Module 1: Basics** 👇
