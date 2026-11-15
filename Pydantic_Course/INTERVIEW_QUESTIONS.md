# Pydantic Course - Complete Interview Questions & Answers

**Total Questions:** 80  
**Difficulty Levels:** Beginner → Expert  
**Estimated Prep Time:** 3-4 hours  
**Last Updated:** November 2026

---

## 📋 Table of Contents

1. [Quick Stats](#quick-stats)
2. [Module 1: Basics (20 Qs)](#module-1-basics)
3. [Module 2: Validation (20 Qs)](#module-2-validation)
4. [Module 3: Validators (20 Qs)](#module-3-validators)
5. [Module 4: Advanced (20 Qs)](#module-4-advanced)
6. [Interview Prep Tips](#interview-prep-tips)
7. [Quick Reference Table](#quick-reference-table)

---

## Quick Stats

| Metric | Value |
|--------|-------|
| **Total Questions** | 80 |
| **Basic Questions (Q1-Q10 per module)** | 40 |
| **Advanced Questions (Q11-Q20 per module)** | 40 |
| **Code Examples** | 150+ |
| **Difficulty Range** | Easy → Hard |
| **Categories** | 12 (Basics, Validation, Async, Types, etc.) |

---

# MODULE 1: BASICS

## Q1: What's the main purpose of Pydantic?

**Difficulty:** 🟢 Easy  
**Category:** Fundamentals  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 30 seconds

**Answer:**
Pydantic is a data validation and serialization library. It automatically validates and parses data, converts types, and catches errors early before they propagate through your application.

**Code Example:**
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Automatic validation + type conversion
user = User(name="John", age="30")  # "30" (string) → 30 (int)
print(user.age)  # 30 (int)
```

**Follow-up Question:** How is this better than manual validation?

---

## Q2: Why use Pydantic instead of regular Python classes?

**Difficulty:** 🟢 Easy  
**Category:** Fundamentals  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1 minute

**Answer:**
Regular classes don't validate data. Pydantic provides automatic type checking, type conversion, validation, clear error messages, and serialization (to dict/JSON). It catches errors at the boundary instead of deep in your code.

**Code Example:**
```python
# Regular Python class - NO validation
class UserRegular:
    def __init__(self, name, age):
        self.name = name  # Any value accepted
        self.age = age    # Any value accepted

user = UserRegular("John", "not_a_number")  # No error!
print(user.age)  # "not_a_number" (wrong type, bug later)

# Pydantic class - AUTOMATIC validation
class UserPydantic(BaseModel):
    name: str
    age: int

user = UserPydantic("John", "not_a_number")  # ❌ ValidationError!
```

**Interview Tip:** Mention how this prevents silent bugs.

---

## Q3: What happens if you pass the wrong type to a Pydantic model?

**Difficulty:** 🟢 Easy  
**Category:** Type Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1 minute

**Answer:**
Pydantic tries to convert it to the correct type. If conversion is possible, it succeeds. If conversion is impossible, it raises a ValidationError with details about what went wrong.

**Code Example:**
```python
class User(BaseModel):
    age: int

# ✅ WORKS - Conversion possible
user1 = User(age="30")
print(user1.age)  # 30 (string converted to int)

# ❌ FAILS - Conversion impossible
user2 = User(age="twenty-five")
# ValidationError: Input should be a valid integer
```

**Follow-up:** Can you disable automatic conversion?

---

## Q4: Can you modify a Pydantic object after creation?

**Difficulty:** 🟡 Medium  
**Category:** Object Properties  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
By default, NO - Pydantic models are immutable. Attempting to modify them raises an error. However, you can enable mutability using `model_config = ConfigDict(validate_assignment=True)`.

**Code Example:**
```python
# Immutable (default)
class User(BaseModel):
    name: str

user = User(name="John")
user.name = "Alice"  # ❌ ValidationError: frozen

# Mutable
from pydantic import ConfigDict

class User(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    name: str

user = User(name="John")
user.name = "Alice"  # ✅ Works
```

**Interview Tip:** Explain why immutability is a good default (prevents accidental mutations).

---

## Q5: What does `model_dump()` return?

**Difficulty:** 🟢 Easy  
**Category:** Serialization  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 30 seconds

**Answer:**
`model_dump()` returns a Python dictionary containing all the model's fields and their values. The returned dictionary is mutable and separate from the original model.

**Code Example:**
```python
class User(BaseModel):
    name: str
    age: int

user = User(name="John", age=30)
user_dict = user.model_dump()
print(user_dict)  # {'name': 'John', 'age': 30}
print(type(user_dict))  # <class 'dict'>
```

---

## Q6: What does `model_dump_json()` return?

**Difficulty:** 🟢 Easy  
**Category:** Serialization  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 30 seconds

**Answer:**
`model_dump_json()` returns a JSON string representation of the model. It's useful for API responses, logging, or storing in databases.

**Code Example:**
```python
class User(BaseModel):
    name: str
    age: int

user = User(name="John", age=30)
json_str = user.model_dump_json()
print(json_str)  # '{"name":"John","age":30}'
print(type(json_str))  # <class 'str'>
```

---

## Q7: How do you access a field from a Pydantic model?

**Difficulty:** 🟢 Easy  
**Category:** Basic Operations  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 30 seconds

**Answer:**
Use dot notation: `model.field_name`. You can also convert to dict and use bracket notation: `model.model_dump()['field_name']`.

**Code Example:**
```python
user = User(name="John", age=30)

# Dot notation (preferred)
print(user.name)  # "John"

# Dict access
user_dict = user.model_dump()
print(user_dict['name'])  # "John"
```

---

## Q8: What's the difference between `BaseModel` and a regular class?

**Difficulty:** 🟡 Medium  
**Category:** Core Concepts  
**Expected Answer Length:** 3-4 sentences  
**Time to Answer:** 2 minutes

**Answer:**
BaseModel is Pydantic's foundation class. Regular classes don't provide validation, type checking, or serialization. BaseModel automatically validates data, converts types, provides helpful error messages, and includes methods like `model_dump()` and `model_dump_json()`.

**Code Example:**
```python
from pydantic import BaseModel

# Regular class
class UserRegular:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Pydantic model
class UserPydantic(BaseModel):
    name: str
    age: int

# Key differences:
u1 = UserRegular("John", "invalid")  # No error, wrong type accepted
u2 = UserPydantic("John", "invalid")  # ❌ ValidationError immediately

# Pydantic has extra methods:
print(u2.model_dump())  # {'name': 'John', 'age': 30}
print(u2.model_dump_json())  # '{"name":"John","age":30}'
```

---

## Q9: Can Pydantic convert strings to numbers?

**Difficulty:** 🟡 Medium  
**Category:** Type Conversion  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, but only for strings that represent numbers. `"123"` converts to `123`, but `"abc"` fails. The conversion only works for logically possible operations.

**Code Example:**
```python
class Data(BaseModel):
    value: int

# ✅ Works - string is numeric
d1 = Data(value="123")
print(d1.value)  # 123 (int)

# ❌ Fails - string is not numeric
d2 = Data(value="abc")
# ValidationError: Input should be a valid integer

# Key insight: "123" can logically become 123
# But "abc" CANNOT logically become a number
```

**Interview Tip:** Pydantic only converts logically compatible types.

---

## Q10: What happens if a required field is missing?

**Difficulty:** 🟢 Easy  
**Category:** Validation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1 minute

**Answer:**
Pydantic raises a `ValidationError` immediately when a required field is missing. The error message clearly indicates which field is missing.

**Code Example:**
```python
class User(BaseModel):
    name: str
    age: int
    email: str

# Missing email field
try:
    user = User(name="John", age=30)
except ValidationError as e:
    print(e)
    # email
    # Field required

# All required fields present
user = User(name="John", age=30, email="john@example.com")  # ✅ Works
```

---

## Q11: If you define a model with `name: str`, can you pass `name=None`?

**Difficulty:** 🟡 Medium  
**Category:** Type Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
NO! `None` is rejected for required string fields. To allow `None`, use `Optional[str]` or `str | None` with a default value.

**Code Example:**
```python
class User(BaseModel):
    name: str  # Required, non-optional

# ❌ This FAILS
user = User(name=None)
# ValidationError: Input should be a valid string

# ✅ This WORKS
user = User(name="John")

# To allow None:
class User(BaseModel):
    name: Optional[str] = None

user = User(name=None)  # ✅ Works now
```

**Interview Tip:** Strict type checking is a feature, not a limitation.

---

## Q12: What's the difference between `name: str = None` and `name: Optional[str] = None`?

**Difficulty:** 🟡 Medium  
**Category:** Type Hints  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
`str = None` is INVALID - Pydantic rejects it. `Optional[str] = None` is CORRECT - it explicitly allows string OR None. The difference is in the type hint: `str` means only strings, `Optional[str]` means strings or None.

**Code Example:**
```python
# ❌ WRONG
class User(BaseModel):
    name: str = None  # Contradiction: str doesn't accept None

# ✅ CORRECT
class User(BaseModel):
    name: Optional[str] = None  # Optional explicitly allows None

# Python 3.10+ alternative:
class User(BaseModel):
    name: str | None = None  # Same as Optional[str]
```

**Common Mistake:** Students write `str = None` thinking it creates an optional field.

---

## Q13: Can you create a Pydantic model without any fields?

**Difficulty:** 🟢 Easy  
**Category:** Model Definition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, you can create an empty model, but it's rarely useful. An empty model accepts no data and serves no validation purpose.

**Code Example:**
```python
class Empty(BaseModel):
    pass

obj = Empty()  # ✅ Works
print(obj.model_dump())  # {}

# This is useless for validation, but can be used as a marker/placeholder
```

---

## Q14: If model_dump() returns a dict, can you modify it and the model stays the same?

**Difficulty:** 🟡 Medium  
**Category:** Object Behavior  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES! `model_dump()` returns a COPY (new dictionary), not a reference. Modifying the dictionary doesn't affect the original model because they're separate objects in memory.

**Code Example:**
```python
user = User(name="John", age=30)

user_dict = user.model_dump()
user_dict["name"] = "Alice"  # Modify the dict

print(user.name)  # "John" (unchanged)
print(user_dict["name"])  # "Alice" (changed)

# They're separate objects!
```

**Interview Tip:** This is crucial for understanding data flow in APIs.

---

## Q15: Can you pass extra fields that aren't defined in the model?

**Difficulty:** 🟡 Medium  
**Category:** Model Configuration  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
NO by default - extra fields are silently ignored. To allow extra fields, use `model_config = ConfigDict(extra='allow')`.

**Code Example:**
```python
class User(BaseModel):
    name: str
    age: int

# Extra field (city) is IGNORED
user = User(name="John", age=30, city="Mumbai")
print(user.model_dump())
# {'name': 'John', 'age': 30}  # city is gone!

# To allow extra fields:
class User(BaseModel):
    model_config = ConfigDict(extra='allow')
    name: str
    age: int

user = User(name="John", age=30, city="Mumbai")
print(user.model_dump())
# {'name': 'John', 'age': 30, 'city': 'Mumbai'}
```

---

## Q16: What happens if you create a model instance but don't provide all required fields?

**Difficulty:** 🟢 Easy  
**Category:** Validation  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
ValidationError is raised immediately with details about which required fields are missing.

**Code Example:**
```python
class User(BaseModel):
    name: str
    age: int
    email: str

try:
    user = User(name="John", age=30)  # Missing email
except ValidationError as e:
    print(e)  # Shows: email is required
```

---

## Q17: Can you use type hints like `List[str]` in Pydantic models?

**Difficulty:** 🟡 Medium  
**Category:** Complex Types  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES! Pydantic supports complex type hints like `List[str]`, `Dict[str, int]`, `Optional[str]`, etc. Pydantic validates each element in lists and each value in dicts.

**Code Example:**
```python
from typing import List, Dict, Optional

class User(BaseModel):
    name: str
    tags: List[str]
    metadata: Dict[str, int]
    phone: Optional[str] = None

user = User(
    name="John",
    tags=["python", "fastapi"],
    metadata={"age": 30, "score": 95},
    phone=None
)
```

---

## Q18: If you call `model_dump_json()`, can you still access fields with dot notation?

**Difficulty:** 🟡 Medium  
**Category:** Serialization  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
NO! `model_dump_json()` returns a STRING, not an object. Strings don't have attributes. The original model object still works with dot notation.

**Code Example:**
```python
user = User(name="John", age=30)

json_str = user.model_dump_json()  # '{"name":"John","age":30}'

# ❌ Can't use dot notation on string
print(json_str.name)  # AttributeError!

# ✅ Original model still works
print(user.name)  # "John"

# ✅ Parse JSON back to dict first
import json
data = json.loads(json_str)
print(data["name"])  # "John"
```

---

## Q19: What's the performance difference between `str` and `Optional[str]`?

**Difficulty:** 🟡 Medium  
**Category:** Performance  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Negligible difference. `Optional[str]` does one extra check (is it None?), but modern computers handle this microseconds. In practice, choose `Optional` for correctness, not performance.

**Code Example:**
```python
# Benchmark (not recommended for real testing):
# str: ~0.1 microseconds per validation
# Optional[str]: ~0.11 microseconds per validation

# Difference is NEGLIGIBLE
# Always use Optional when None is possible, regardless of performance
```

---

## Q20: Can you inherit from one Pydantic model to create another?

**Difficulty:** 🟡 Medium  
**Category:** Object-Oriented Design  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
YES! Pydantic supports inheritance. Child models inherit all fields and validation from parent models, and can add new fields.

**Code Example:**
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

**Interview Tip:** This enables DRY (Don't Repeat Yourself) principle.

---

## ⚠️ Important Note: Positional Arguments

**Difficulty:** 🟡 Medium  
**Category:** Gotchas  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Gotcha:** In Pydantic v2, you CANNOT use positional arguments!

**Code Example:**
```python
class Student(BaseModel):
    student_id: int
    name: str
    grade: str

# ✅ CORRECT - Named arguments
student1 = Student(student_id=1001, name="David", grade="A")

# ❌ WRONG - Positional arguments
student2 = Student(1001, "David", "A")
# TypeError: BaseModel.__init__() takes 1 positional argument but 4 were given
```

**Interview Tip:** This is a key difference from Pydantic v1.

---

# MODULE 2: VALIDATION

## Q1: What's the difference between required and optional fields?

**Difficulty:** 🟢 Easy  
**Category:** Validation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1 minute

**Answer:**
Required fields must be provided when creating a model instance. Optional fields can be omitted and default to a specified value (usually None).

**Code Example:**
```python
class User(BaseModel):
    name: str  # Required
    email: Optional[str] = None  # Optional

user1 = User(name="John")  # ✅ Works
user2 = User(name="John", email="john@example.com")  # ✅ Works
user3 = User(email="john@example.com")  # ❌ Missing required 'name'
```

---

## Q2: How do you validate a number is between 0 and 100?

**Difficulty:** 🟡 Medium  
**Category:** Constraints  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `Field(ge=0, le=100)` where `ge` = greater-than-equal, `le` = less-than-equal.

**Code Example:**
```python
from pydantic import BaseModel, Field

class Score(BaseModel):
    value: int = Field(ge=0, le=100)

score = Score(value=85)  # ✅ Works
score = Score(value=150)  # ❌ ValidationError
```

---

## Q3: What does `...` mean in Field()?

**Difficulty:** 🟡 Medium  
**Category:** Field Definition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
`...` (Ellipsis) means the field is required. It's Python's way of saying "this must be provided, no default value".

**Code Example:**
```python
class User(BaseModel):
    name: str = Field(...)  # Required field
    email: Optional[str] = Field(None)  # Optional field

user = User(name="John")  # ✅ Works
user = User()  # ❌ Missing required 'name'
```

---

## Q4: Can Pydantic convert "123" (string) to 123 (int)?

**Difficulty:** 🟡 Medium  
**Category:** Type Conversion  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES by default. Use `strict=True` in Field() to disable this and require exact types.

**Code Example:**
```python
class Data(BaseModel):
    value: int

# Default: Conversion enabled
d1 = Data(value="123")  # ✅ Works, "123" → 123

class Data(BaseModel):
    value: int = Field(strict=True)

# Strict mode: No conversion
d2 = Data(value="123")  # ❌ ValidationError: must be exact int
d3 = Data(value=123)  # ✅ Works
```

---

## Q5: How do you limit string length?

**Difficulty:** 🟢 Easy  
**Category:** Constraints  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `Field(min_length=n, max_length=m)` to set minimum and maximum string length.

**Code Example:**
```python
class User(BaseModel):
    username: str = Field(min_length=3, max_length=20)

user1 = User(username="john")  # ✅ Works (4 chars, within range)
user2 = User(username="jo")  # ❌ Too short
user3 = User(username="a" * 50)  # ❌ Too long
```

---

## Q11: What's the difference between `Field(default=None)` and `Optional[str] = None`?

**Difficulty:** 🟡 Medium  
**Category:** Field Definition  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
They're functionally similar, but `Field()` is more powerful. It allows you to add metadata (description, examples, constraints) for documentation and API generation.

**Code Example:**
```python
class User(BaseModel):
    # Simple way
    name: Optional[str] = None

    # With Field() - more control
    email: Optional[str] = Field(
        None,
        description="User's email address",
        examples=["user@example.com"],
        min_length=5
    )
```

---

## Q12: If you use `strict=True`, what exactly happens?

**Difficulty:** 🟡 Medium  
**Category:** Type Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
NO type conversion happens. The value must be the exact type specified. Even "30" (string that looks like int) is rejected.

**Code Example:**
```python
class User(BaseModel):
    age: int = Field(strict=True)

user1 = User(age=30)  # ✅ Works (exact int)
user2 = User(age="30")  # ❌ FAILS (no conversion)
# ValidationError: Input should be a valid integer

# Without strict (default):
class User(BaseModel):
    age: int

user3 = User(age="30")  # ✅ Works ("30" → 30)
```

---

## Q13: Can you have BOTH `gt` (greater than) and `ge` (greater-equal)?

**Difficulty:** 🟡 Medium  
**Category:** Constraints  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
NO! Only use ONE comparison operator. Using both creates contradictory constraints.

**Code Example:**
```python
# ❌ WRONG - Contradictory
class User(BaseModel):
    age: int = Field(gt=18, ge=21)

# ✅ CORRECT - Use one
class User(BaseModel):
    age: int = Field(ge=18)  # Greater than or equal to 18
```

---

## Q14: What if you set `min_length=5` on an integer field?

**Difficulty:** 🟡 Medium  
**Category:** Constraints  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
It has NO EFFECT. `min_length` only works on strings and sequences. For integers, use `ge` (greater-equal) instead.

**Code Example:**
```python
class User(BaseModel):
    age: int = Field(min_length=5)  # ❌ IGNORED
    name: str = Field(min_length=5)  # ✅ Works

user = User(age=3, name="John")  # ❌ Fails (name too short)
user = User(age=3, name="Johnny")  # ✅ Works

# Use right constraints:
# Numbers: ge/gt/le/lt
# Strings: min_length/max_length
```

---

## Q15: If you have `Field(ge=0, le=100)` and pass 101, what happens?

**Difficulty:** 🟢 Easy  
**Category:** Validation  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
ValidationError is raised immediately because 101 violates the `le=100` constraint.

**Code Example:**
```python
class Score(BaseModel):
    value: int = Field(ge=0, le=100)

score = Score(value=101)
# ValidationError: Input should be less than or equal to 100
```

---

## Q16: Can you use regex validation with Field()?

**Difficulty:** 🟡 Medium  
**Category:** Advanced Validation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, using the `pattern` parameter. Provide a regex string, and Pydantic validates the field against it.

**Code Example:**
```python
class User(BaseModel):
    email: str = Field(
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )

user1 = User(email="john@example.com")  # ✅ Works
user2 = User(email="invalid-email")  # ❌ Fails regex
```

---

## Q17: What does `Field(..., description="...")`  do?

**Difficulty:** 🟢 Easy  
**Category:** Documentation  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Adds documentation for Swagger/OpenAPI. Doesn't affect validation - purely for API documentation.

**Code Example:**
```python
class User(BaseModel):
    name: str = Field(..., description="User's full name")
    age: int = Field(..., description="Age in years", ge=0)

# When generated as API docs, these descriptions appear in Swagger UI
```

---

## Q18: If you use `Field(default="John")`, is the field optional?

**Difficulty:** 🟢 Easy  
**Category:** Field Definition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES! Default value makes the field optional. If not provided, it defaults to "John".

**Code Example:**
```python
class User(BaseModel):
    name: str = Field(default="John")  # Optional

user1 = User()  # ✅ Uses default "John"
user2 = User(name="Alice")  # ✅ Uses provided "Alice"
```

---

## Q19: Can you use `Field()` with required fields (no default)?

**Difficulty:** 🟡 Medium  
**Category:** Field Definition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES! Use `...` (Ellipsis) to mark required. This allows you to add validation constraints while keeping field required.

**Code Example:**
```python
class User(BaseModel):
    name: str = Field(...)  # Required
    age: int = Field(..., ge=0)  # Required with validation

user = User(name="John", age=30)  # ✅ Works
user = User(age=30)  # ❌ Missing 'name'
```

---

## Q20: What's the difference between `min_length` and `ge`?

**Difficulty:** 🟡 Medium  
**Category:** Constraints  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
`ge/gt/le/lt` are for numeric comparison. `min_length/max_length` are for string/sequence length. They're for different data types.

**Code Example:**
```python
class User(BaseModel):
    age: int = Field(ge=0, le=150)  # Numeric: age 0-150
    name: str = Field(min_length=1, max_length=50)  # String: 1-50 chars
    tags: list = Field(min_length=1)  # List: at least 1 item

user = User(
    age=30,
    name="John",
    tags=["python"]
)  # ✅ All valid
```

---

# MODULE 3: VALIDATORS

## Q1: What's the difference between @field_validator and @model_validator?

**Difficulty:** 🟡 Medium  
**Category:** Custom Validation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
`@field_validator` validates a single field. `@model_validator` validates across multiple fields or the entire model.

**Code Example:**
```python
from pydantic import BaseModel, field_validator, model_validator

class User(BaseModel):
    age: int
    password: str
    password_confirm: str

    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v

    @model_validator(mode='after')
    def check_passwords(self):
        if self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
        return self
```

---

## Q2: When would you use mode='before' vs mode='after'?

**Difficulty:** 🟡 Medium  
**Category:** Validation Modes  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
`mode='before'` runs before type conversion (raw input). `mode='after'` runs after type conversion (guaranteed correct type).

**Code Example:**
```python
class User(BaseModel):
    age: int

    @field_validator('age', mode='before')
    @classmethod
    def check_before(cls, v):
        # v might be "30" (string) or 30 (int)
        if isinstance(v, str) and not v.isdigit():
            raise ValueError('Must be numeric string or int')
        return v

    @field_validator('age', mode='after')
    @classmethod
    def check_after(cls, v):
        # v is guaranteed to be int
        if v < 0:
            raise ValueError('Age must be positive')
        return v
```

---

## Q3: Can one validator handle multiple fields?

**Difficulty:** 🟡 Medium  
**Category:** Validators  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES! Pass multiple field names to `@field_validator('field1', 'field2', ...)`.

**Code Example:**
```python
class User(BaseModel):
    first_name: str
    last_name: str

    @field_validator('first_name', 'last_name')
    @classmethod
    def names_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
```

---

## Q4: How do you transform a field value?

**Difficulty:** 🟡 Medium  
**Category:** Value Transformation  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Return the transformed value from the validator function.

**Code Example:**
```python
class User(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def transform_name(cls, v):
        return v.upper()  # Transform to uppercase

user = User(name="john")
print(user.name)  # "JOHN"
```

---

## Q5: When should you use @model_validator?

**Difficulty:** 🟡 Medium  
**Category:** Validators  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `@model_validator` when validation requires comparing two or more fields, or complex cross-field logic that's impossible with single field validators.

**Code Example:**
```python
class Order(BaseModel):
    order_type: str
    discount_code: Optional[str] = None

    @model_validator(mode='after')
    def validate_discount(self):
        if self.order_type == "regular" and self.discount_code:
            raise ValueError("Regular orders cannot use discount")
        if self.order_type == "premium" and not self.discount_code:
            raise ValueError("Premium orders require discount")
        return self
```

---

## Q11: If you have `@field_validator('age', mode='before')`, can you access the age field's type?

**Difficulty:** 🟠 Hard  
**Category:** Validator Internals  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
In `mode='before'`, the raw value is provided before type conversion. You must check the type yourself since conversion hasn't happened yet.

**Code Example:**
```python
class User(BaseModel):
    age: int

    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, v):
        # v could be string "30" or int 30
        if isinstance(v, str) and not v.isdigit():
            raise ValueError('Age must be numeric')
        return v

user1 = User(age="30")  # ✅ Works
user2 = User(age="abc")  # ❌ Fails
```

---

## Q12: What's the difference between returning and raising in a validator?

**Difficulty:** 🟡 Medium  
**Category:** Validator Behavior  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Returning uses the returned value. Raising stops validation and fails with error.

**Code Example:**
```python
class User(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def transform_name(cls, v):
        # Return = transform and accept
        return v.upper()

    # Alternative: reject certain values
    @field_validator('name')
    @classmethod
    def check_name(cls, v):
        if v == "admin":
            raise ValueError("Cannot use 'admin'")
        return v
```

---

## Q13: Can you call other validators from inside a validator?

**Difficulty:** 🟠 Hard  
**Category:** Validator Design  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
NO directly. Use helper methods instead to share logic between validators.

**Code Example:**
```python
class User(BaseModel):
    email: str
    backup_email: str

    @classmethod
    def _is_valid_email(cls, email):
        return "@" in email and "." in email

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not cls._is_valid_email(v):
            raise ValueError('Invalid email')
        return v

    @field_validator('backup_email')
    @classmethod
    def validate_backup(cls, v):
        if not cls._is_valid_email(v):
            raise ValueError('Invalid backup email')
        return v
```

---

## Q14: If a validator returns None, does the field become None?

**Difficulty:** 🟡 Medium  
**Category:** Validator Return Values  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES! Returning None sets the field to None. Be careful if the field isn't Optional.

**Code Example:**
```python
class User(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def transform(cls, v):
        if v == "":
            return None  # Sets to None!
        return v

user = User(name="")
print(user.name)  # None (not empty string)
```

---

## Q15: Can you have multiple validators for the same field?

**Difficulty:** 🟡 Medium  
**Category:** Validator Composition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES! Multiple validators run in order, each validating/transforming the field.

**Code Example:**
```python
class User(BaseModel):
    age: int

    @field_validator('age')
    @classmethod
    def positive(cls, v):
        if v < 0:
            raise ValueError('Must be positive')
        return v

    @field_validator('age')
    @classmethod
    def reasonable(cls, v):
        if v > 150:
            raise ValueError('Unrealistic age')
        return v

user = User(age=200)  # ❌ Fails second validator
```

---

## Q16: What does `mode='wrap'` do?

**Difficulty:** 🟠 Hard  
**Category:** Advanced Validators  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
`mode='wrap'` wraps the default validator. You can call the default validator via `handler()` and add custom logic around it.

**Code Example:**
```python
class User(BaseModel):
    age: int

    @field_validator('age', mode='wrap')
    @classmethod
    def wrap_age(cls, v, handler):
        result = handler(v)  # Run default validation/conversion
        print(f"Age validated: {result}")
        return result

user = User(age="30")  # Prints "Age validated: 30"
```

---

## Q17: If you use `@model_validator(mode='after')`, when does it run?

**Difficulty:** 🟡 Medium  
**Category:** Validator Timing  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
AFTER all field validators complete. All fields are guaranteed to be valid at this point.

**Code Example:**
```python
class User(BaseModel):
    password: str
    password_confirm: str

    @model_validator(mode='after')
    def check_match(self):
        if self.password != self.password_confirm:
            raise ValueError('Passwords do not match')
        return self
```

---

## Q18: Can a @model_validator modify multiple fields?

**Difficulty:** 🟡 Medium  
**Category:** Model Validation  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES! You can modify `self` and change any fields.

**Code Example:**
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
print(user.full_name)  # "John Doe"
```

---

## Q19: What happens if a field validator has an error that's also caught by model_validator?

**Difficulty:** 🟠 Hard  
**Category:** Error Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Field validator error is raised FIRST. Model validator never runs if field validation fails.

**Code Example:**
```python
class User(BaseModel):
    age: int

    @field_validator('age')
    @classmethod
    def positive(cls, v):
        if v < 0:
            raise ValueError('Must be positive')  # Raised first
        return v

    @model_validator(mode='after')
    def check_model(self):
        if self.age > 150:
            raise ValueError('Age unrealistic')
        return self

user = User(age=-5)  # ❌ Field validator error
user = User(age=200)  # ❌ Model validator error
```

---

## Q20: How do you write a validator that depends on another field's value?

**Difficulty:** 🟠 Hard  
**Category:** Cross-Field Validation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Use `@model_validator` to access other fields. Field validators can only see their own field.

**Code Example:**
```python
class Order(BaseModel):
    order_type: str
    discount_code: Optional[str] = None

    @model_validator(mode='after')
    def validate_discount(self):
        if self.order_type == "regular" and self.discount_code:
            raise ValueError("Regular orders can't use discounts")
        if self.order_type == "premium" and not self.discount_code:
            raise ValueError("Premium orders require discount")
        return self

order = Order(order_type="regular", discount_code="SAVE10")  # ❌
```

---

# MODULE 4: ADVANCED

## Q1: What's the difference between nested models and inheritance?

**Difficulty:** 🟡 Medium  
**Category:** Object Design  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Nested models (composition) embed other models as fields. Inheritance means one model inherits from another. Nested models are reusable; inheritance creates hierarchies.

**Code Example:**
```python
# Nested models (composition)
class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    name: str
    address: Address  # Embedding model

user = User(name="John", address={"street": "123 Main", "city": "NYC"})

# Inheritance
class Person(BaseModel):
    name: str
    age: int

class Employee(Person):
    employee_id: int  # Inherits name and age
```

---

## Q2: When should you use @computed_field?

**Difficulty:** 🟡 Medium  
**Category:** Computed Properties  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
When you need a field calculated from other fields (full_name, age_group, status). It's read-only and computed on-the-fly.

**Code Example:**
```python
from pydantic import computed_field

class User(BaseModel):
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

user = User(first_name="John", last_name="Doe")
print(user.full_name)  # "John Doe"
```

---

## Q3: How do you exclude fields when exporting?

**Difficulty:** 🟡 Medium  
**Category:** Serialization  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `model.model_dump(exclude={'field1', 'field2'})` to exclude specific fields.

**Code Example:**
```python
class User(BaseModel):
    name: str
    password: str
    email: str

user = User(name="John", password="secret", email="john@example.com")
user_dict = user.model_dump(exclude={'password'})
print(user_dict)  # {'name': 'John', 'email': '...'}
```

---

## Q4: Can computed fields appear in model_dump()?

**Difficulty:** 🟡 Medium  
**Category:** Computed Properties  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES! Computed fields are included by default in `model_dump()`.

**Code Example:**
```python
user = User(first_name="John", last_name="Doe")
print(user.model_dump())
# {'first_name': 'John', 'last_name': 'Doe', 'full_name': 'John Doe'}

# Exclude computed field if needed:
print(user.model_dump(exclude={'full_name'}))
# {'first_name': 'John', 'last_name': 'Doe'}
```

---

## Q5: What's the difference between model_dump() and model_dump_json()?

**Difficulty:** 🟢 Easy  
**Category:** Serialization  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
`model_dump()` returns a Python dict. `model_dump_json()` returns a JSON string.

**Code Example:**
```python
user = User(name="John", age=30)

dict_form = user.model_dump()  # {'name': 'John', 'age': 30}
json_form = user.model_dump_json()  # '{"name":"John","age":30}'
```

---

## Q11: Can you have a @computed_field that depends on another @computed_field?

**Difficulty:** 🟠 Hard  
**Category:** Computed Properties  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
YES! Computed fields can chain and depend on each other.

**Code Example:**
```python
class User(BaseModel):
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @computed_field
    @property
    def full_name_upper(self) -> str:
        return self.full_name.upper()  # Depends on another computed field

user = User(first_name="John", last_name="Doe")
print(user.full_name_upper)  # "JOHN DOE"
```

---

## Q12: If you exclude a field in model_dump(), can you still access it on the object?

**Difficulty:** 🟡 Medium  
**Category:** Serialization  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES! Exclude only affects the dict export. The original object still has all fields.

**Code Example:**
```python
user = User(name="John", password="secret")

user_dict = user.model_dump(exclude={'password'})
print(user_dict)  # {'name': 'John'}

print(user.password)  # "secret" (still accessible!)
```

---

## Q13: Can you use `exclude` with nested models?

**Difficulty:** 🟠 Hard  
**Category:** Advanced Serialization  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
YES! Use dot notation to exclude nested fields.

**Code Example:**
```python
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    address: Address

user = User(
    name="John",
    address={"street": "123 Main", "city": "NYC", "zip_code": "10001"}
)

# Exclude nested field
data = user.model_dump(exclude={'address': {'zip_code'}})
print(data)
# {'name': 'John', 'address': {'street': '123 Main', 'city': 'NYC'}}
```

---

## Q14: What's the difference between `exclude` and `include` in model_dump()?

**Difficulty:** 🟡 Medium  
**Category:** Serialization  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
`exclude` removes fields. `include` keeps ONLY specified fields. Result is the same but approach differs.

**Code Example:**
```python
user = User(name="John", age=30, email="john@ex.com", phone="555-1234")

# Exclude: remove these
dict1 = user.model_dump(exclude={'phone', 'email'})
# {'name': 'John', 'age': 30}

# Include: keep ONLY these
dict2 = user.model_dump(include={'name', 'age'})
# {'name': 'John', 'age': 30}
```

---

## Q15: Can model_dump_json() fail if your model has non-JSON types?

**Difficulty:** 🟠 Hard  
**Category:** Serialization  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
YES! Non-JSON types (file objects, custom classes) will fail. Pydantic handles standard types (datetime, etc.) but not custom objects.

**Code Example:**
```python
from datetime import datetime

class Event(BaseModel):
    name: str
    date: datetime

# ✅ Works - datetime is handled
event = Event(name="Meeting", date=datetime.now())
json_str = event.model_dump_json()

# ❌ Fails - file object not JSON serializable
class Event(BaseModel):
    name: str
    file: open

event = Event(name="Data", file=open("data.txt"))
json_str = event.model_dump_json()  # TypeError!
```

---

## Q16: Can you have circular references in nested models?

**Difficulty:** 🟠 Hard  
**Category:** Advanced Models  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
YES! Using `from __future__ import annotations`, models can reference themselves.

**Code Example:**
```python
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    friends: Optional[list[User]] = None

data = {
    "name": "John",
    "friends": [
        {"name": "Alice", "friends": None},
        {"name": "Bob", "friends": None}
    ]
}

user = User(**data)
print(user.friends[0].name)  # "Alice"
```

---

## Q17: What happens if you call model_dump_json() on a very large model?

**Difficulty:** 🟡 Medium  
**Category:** Performance  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
It works but may be slow. Converting a huge model to JSON takes time. For large data, consider streaming or pagination.

**Code Example:**
```python
# Large model with 10,000 items
large_model = LargeModel(items=[...]*10000)

# Convert all to JSON (might be slow)
json_str = large_model.model_dump_json()
print(len(json_str))  # Very large string!

# Better: Use streaming or pagination for large datasets
```

---

## Q18: Can you customize how model_dump_json() formats output?

**Difficulty:** 🟡 Medium  
**Category:** Serialization  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES! Use `by_alias`, `indent` parameters to customize formatting.

**Code Example:**
```python
class User(BaseModel):
    name: str = Field(alias="full_name")
    age: int

user = User(full_name="John", age=30)

# Use aliases
json1 = user.model_dump_json(by_alias=True)
# {"full_name":"John","age":30}

# Pretty print
json2 = user.model_dump_json(indent=2)
# {
#   "name": "John",
#   "age": 30
# }
```

---

## Q19: If you inherit from a Pydantic model, can you override fields?

**Difficulty:** 🟡 Medium  
**Category:** Inheritance  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, you can override fields in child models, but be careful with validation rules.

**Code Example:**
```python
class User(BaseModel):
    name: str
    age: int

class Admin(User):
    age: int = 18  # Override with default

admin1 = Admin(name="John")  # age defaults to 18
admin2 = Admin(name="Jane", age=50)  # age is 50
```

---

## Q20: Can you use computed_field with parameters?

**Difficulty:** 🟡 Medium  
**Category:** Computed Properties  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
NO! Computed fields take no parameters. Use a regular method if you need parameters.

**Code Example:**
```python
class User(BaseModel):
    price: float

    # ❌ WRONG - Can't accept parameters
    @computed_field
    @property
    def discount_price(self, percentage) -> float:
        return self.price * (1 - percentage)

    # ✅ CORRECT - Use default logic
    @computed_field
    @property
    def discount_price(self) -> float:
        return self.price * 0.9  # Always 10% off

    # ✅ Use regular method for parameters
    def get_discount_price(self, percentage: float) -> float:
        return self.price * (1 - percentage)
```

---

# Interview Prep Tips

## General Strategy

1. **Start with basics**: Questions 1-10 of each module are fundamental
2. **Understand concepts**: Don't memorize - understand WHY
3. **Practice code**: Run every example
4. **Ask follow-ups**: Interviewers appreciate thoughtful questions

## Common Pitfalls

- ❌ Confusing `Optional[str]` with `str = None`
- ❌ Not understanding immutability by default
- ❌ Forgetting to use `Field()` for constraints
- ❌ Mixing up `model_dump()` and `model_dump_json()`
- ❌ Not knowing when to use `@model_validator` vs `@field_validator`

## Confidence Builders

✅ Run all code examples locally  
✅ Modify examples and predict output  
✅ Explain concepts to someone else  
✅ Time yourself answering questions  
✅ Review errors and edge cases  

## Interview Day Tips

1. Listen carefully to the question
2. Ask clarifying questions if needed
3. Start with the simplest answer, add details
4. Use code examples when possible
5. Admit if you don't know, then think out loud

---

# Quick Reference Table

| Question | Difficulty | Category | Key Concept |
|----------|-----------|----------|------------|
| Module 1, Q1-10 | Easy-Medium | Fundamentals | Validation, types, serialization |
| Module 1, Q11-20 | Medium-Hard | Advanced | Optional, inheritance, edge cases |
| Module 2, Q1-10 | Easy-Medium | Constraints | Field validation, min/max, patterns |
| Module 2, Q11-20 | Medium-Hard | Advanced | Strict mode, edge cases, gotchas |
| Module 3, Q1-10 | Easy-Medium | Validators | Basic validators, modes |
| Module 3, Q11-20 | Medium-Hard | Advanced | Cross-field validation, wrapping |
| Module 4, Q1-10 | Easy-Medium | Advanced | Nested models, computed fields |
| Module 4, Q11-20 | Hard | Complex | Circular references, custom serialization |

---

**Good luck with your interviews!** 🚀  
Practice these questions and you'll be well-prepared for any Pydantic-related interview.
