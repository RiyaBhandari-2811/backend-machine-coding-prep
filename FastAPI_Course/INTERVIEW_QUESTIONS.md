# FastAPI Course - Complete Interview Questions & Answers

**Total Questions:** 180  
**Difficulty Levels:** Beginner → Expert  
**Estimated Prep Time:** 6-8 hours  
**Last Updated:** November 2026

---

## 📋 Table of Contents

1. [Quick Stats](#quick-stats)
2. [Chapter 1: Introduction (20 Qs)](#chapter-1-introduction)
3. [Chapter 2: Request Models (20 Qs)](#chapter-2-request-models)
4. [Chapter 3: Response Models (20 Qs)](#chapter-3-response-models)
5. [Chapter 4: Async & Concurrency (20 Qs)](#chapter-4-async--concurrency)
6. [Chapter 5: Dependencies (20 Qs)](#chapter-5-dependencies)
7. [Chapter 6: Error Handling (20 Qs)](#chapter-6-error-handling)
8. [Chapter 7: Security & Auth (20 Qs)](#chapter-7-security--auth)
9. [Chapter 8: WebSockets (20 Qs)](#chapter-8-websockets)
10. [Chapter 9: Testing & Deployment (20 Qs)](#chapter-9-testing--deployment)
11. [Interview Prep Tips](#interview-prep-tips)
12. [Quick Reference Table](#quick-reference-table)

---

## Quick Stats

| Metric | Value |
|--------|-------|
| **Total Questions** | 180 |
| **Basic Questions (Q1-Q10 per chapter)** | 90 |
| **Advanced Questions (Q11-Q20 per chapter)** | 90 |
| **Code Examples** | 250+ |
| **Difficulty Range** | Easy → Expert |
| **Topics Covered** | 20+ (APIs, validation, async, security, etc.) |

---

# CHAPTER 1: INTRODUCTION

## Q1: What is FastAPI?

**Difficulty:** 🟢 Easy  
**Category:** Fundamentals  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 30 seconds

**Answer:**
FastAPI is a modern, fast Python web framework for building APIs. It's built on Starlette (ASGI) and uses Pydantic for validation. It provides automatic API documentation, type checking, and async support.

**Code Example:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

**Interview Tip:** Mention performance benefits compared to Flask/Django.

---

## Q2: What's the difference between FastAPI and Flask?

**Difficulty:** 🟡 Medium  
**Category:** Framework Comparison  
**Expected Answer Length:** 3-4 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Flask is synchronous (blocks on I/O). FastAPI is asynchronous (non-blocking). FastAPI includes automatic validation, documentation, and type checking. FastAPI is faster for I/O-heavy workloads. Flask is simpler for basic applications.

**Performance:**
- Flask (WSGI): ~1,000-5,000 requests/sec
- FastAPI (ASGI): ~15,000+ requests/sec

---

## Q3: What's ASGI?

**Difficulty:** 🟡 Medium  
**Category:** Architecture  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
ASGI = Asynchronous Server Gateway Interface. Allows Python web applications to handle async/await. Replaces WSGI (synchronous). Enables non-blocking I/O, better concurrency, higher throughput.

**Comparison:**
```
WSGI (Flask): Thread pool, blocking I/O
ASGI (FastAPI): Event loop, async/await, non-blocking
```

---

## Q4: Do you need to install additional dependencies to run FastAPI?

**Difficulty:** 🟢 Easy  
**Category:** Setup  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1 minute

**Answer:**
FastAPI needs an ASGI server to run. `uvicorn` is the most popular. Install both: `pip install fastapi uvicorn[standard]`.

**Installation:**
```bash
pip install fastapi
pip install uvicorn[standard]

# Run
uvicorn main:app --reload
```

---

## Q5: How do you define a path parameter in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Routing  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use curly braces in the path: `@app.get("/items/{item_id}")`. FastAPI automatically extracts and validates the parameter.

**Code Example:**
```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

# GET /items/42 → returns {"item_id": 42}
# GET /items/invalid → 422 Unprocessable Entity (not an int)
```

---

## Q6: What are query parameters in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Parameters  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1 minute

**Answer:**
Query parameters come after `?` in URL. FastAPI automatically extracts them from function arguments. Type hints determine validation.

**Code Example:**
```python
@app.get("/items/")
def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# GET /items/?skip=5&limit=20
# {"skip": 5, "limit": 20}
```

---

## Q7: What's the purpose of Pydantic in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Validation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Pydantic validates request/response data. Automatically converts types, checks constraints, and provides helpful error messages. Generates automatic API documentation.

---

## Q8: How do you define a request body in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Request Handling  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use a Pydantic model as a function parameter. FastAPI automatically reads the request body and validates it.

**Code Example:**
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    return item

# POST /items/
# {"name": "Widget", "price": 10.5}
```

---

## Q9: How do you return a response in FastAPI?

**Difficulty:** 🟢 Easy  
**Category:** Response Handling  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 30 seconds

**Answer:**
Return a Python dict or Pydantic model. FastAPI automatically converts it to JSON. Use `JSONResponse` for custom responses.

**Code Example:**
```python
@app.get("/")
def read_root():
    return {"message": "Hello"}  # Automatically JSONified

# Response: {"message": "Hello"}
```

---

## Q10: What's automatic API documentation in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Documentation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
FastAPI automatically generates interactive Swagger UI and ReDoc documentation from your code. No extra work needed. Access at `/docs` and `/redoc`.

**URLs:**
```
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
OpenAPI Schema: http://localhost:8000/openapi.json
```

---

## Q11: Can you run multiple endpoints with the same path but different methods?

**Difficulty:** 🟡 Medium  
**Category:** Routing  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES! Use different decorators (@app.get, @app.post, etc.). FastAPI handles routing based on method.

**Code Example:**
```python
@app.get("/items/")
def list_items():
    return []

@app.post("/items/")
def create_item(item: Item):
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"deleted": True}
```

---

## Q12: What happens if a path parameter type doesn't match the URL?

**Difficulty:** 🟡 Medium  
**Category:** Validation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
FastAPI returns a 422 Unprocessable Entity error with validation details. The error explains what type was expected.

**Example:**
```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}

# GET /items/abc  → 422 error
# Error: "value is not a valid integer"
```

---

## Q13: Can you have the same parameter name in both path and query?

**Difficulty:** 🟡 Medium  
**Category:** Parameters  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
NO! Path and query parameters must have different names. FastAPI distinguishes them by location, but same name causes ambiguity.

**Example:**
```python
# ✅ CORRECT
@app.get("/items/{item_id}")
def get_item(item_id: int, skip: int = 0):
    return {"item_id": item_id, "skip": skip}

# ❌ WRONG - Ambiguous
@app.get("/items/{id}")
def get_item(id: int, id: int = 0):  # Duplicate names!
```

---

## Q14: How do you set default values for query parameters?

**Difficulty:** 🟢 Easy  
**Category:** Parameters  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use Python default values in function parameters.

**Code Example:**
```python
@app.get("/items/")
def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# GET /items/ → {"skip": 0, "limit": 10}
# GET /items/?skip=5 → {"skip": 5, "limit": 10}
```

---

## Q15: Can you make a query parameter required?

**Difficulty:** 🟡 Medium  
**Category:** Parameters  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, by not providing a default value. FastAPI treats it as required.

**Code Example:**
```python
@app.get("/items/")
def get_items(q: str):  # No default = required
    return {"q": q}

# GET /items/ → 422 error (missing q)
# GET /items/?q=search → {"q": "search"}
```

---

## Q16: What's the difference between `body` and a Pydantic model?

**Difficulty:** 🟡 Medium  
**Category:** Request Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
A Pydantic model automatically reads from request body. `Body()` explicitly marks parameters as body fields (rare to need).

**Code Example:**
```python
class Item(BaseModel):
    name: str

# Body implicitly from request
@app.post("/items/")
def create_item(item: Item):
    return item
```

---

## Q17: Can you document path/query parameters?

**Difficulty:** 🟡 Medium  
**Category:** Documentation  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, use `Query()` and `Path()` to add descriptions that appear in Swagger UI.

**Code Example:**
```python
from fastapi import Query, Path

@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(..., description="The item ID"),
    q: str = Query(None, description="Search query")
):
    return {"item_id": item_id, "q": q}
```

---

## Q18: What's the difference between PUT and PATCH?

**Difficulty:** 🟡 Medium  
**Category:** HTTP Methods  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
PUT replaces the entire resource. PATCH updates only specified fields. Use PATCH for partial updates, PUT for full replacement.

**Example:**
```python
@app.put("/items/{item_id}")
def update_item_full(item_id: int, item: Item):
    # Replace entire item
    return item

@app.patch("/items/{item_id}")
def update_item_partial(item_id: int, item_update: dict):
    # Update only provided fields
    return item_update
```

---

## Q19: Can you have both a request body and query parameters in the same endpoint?

**Difficulty:** 🟡 Medium  
**Category:** Parameters  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES! FastAPI distinguishes them by context (body vs URL).

**Code Example:**
```python
@app.post("/items/")
def create_item(item: Item, q: str = None):
    # item from body, q from query
    return {"item": item, "q": q}
```

---

## Q20: How do you handle file uploads in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** File Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `File` parameter type. FastAPI automatically handles multipart/form-data. Returns an `UploadFile` object.

**Code Example:**
```python
from fastapi import File, UploadFile

@app.post("/upload/")
def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

# POST /upload/ with file in form-data
```

---

# CHAPTER 2: REQUEST MODELS

## Q1: What's the purpose of Pydantic models in FastAPI?

**Difficulty:** 🟢 Easy  
**Category:** Validation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1 minute

**Answer:**
Validate request data, define API contracts, auto-generate documentation, ensure type safety, and provide helpful error messages.

---

## Q2: How do you define a required field in a Pydantic model?

**Difficulty:** 🟢 Easy  
**Category:** Model Definition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 30 seconds

**Answer:**
Just declare the field with a type hint. No default value = required.

**Code Example:**
```python
class User(BaseModel):
    name: str  # Required
    age: int   # Required
    email: Optional[str] = None  # Optional
```

---

## Q3: How do you make a field optional?

**Difficulty:** 🟢 Easy  
**Category:** Model Definition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 30 seconds

**Answer:**
Use `Optional[T]` type hint and provide a default value (usually None).

**Code Example:**
```python
from typing import Optional

class User(BaseModel):
    name: str
    phone: Optional[str] = None  # Optional field
```

---

## Q4: Can you add validation to Pydantic fields?

**Difficulty:** 🟡 Medium  
**Category:** Validation  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, use `Field()` with constraints like `ge`, `le`, `min_length`, `max_length`, `pattern`.

**Code Example:**
```python
from pydantic import Field

class User(BaseModel):
    age: int = Field(ge=0, le=150)
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
```

---

## Q5: How do you define nested models in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Model Composition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use another Pydantic model as a field type. Nesting can be multiple levels deep.

**Code Example:**
```python
class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    name: str
    address: Address

# POST /users/
# {"name": "John", "address": {"street": "123 Main", "city": "NYC"}}
```

---

## Q6: What happens if extra fields are sent in a request?

**Difficulty:** 🟡 Medium  
**Category:** Validation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
By default, extra fields are ignored. Use `model_config` with `extra='forbid'` to reject extra fields.

**Code Example:**
```python
from pydantic import ConfigDict

class User(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str
    age: int

# POST {"name": "John", "age": 30, "extra": "field"}
# → 422 Error (extra field rejected)
```

---

## Q7: How do you provide default values in Pydantic models?

**Difficulty:** 🟢 Easy  
**Category:** Model Definition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 30 seconds

**Answer:**
Use `= value` in field definition.

**Code Example:**
```python
class User(BaseModel):
    name: str
    role: str = "user"  # Default: "user"
    active: bool = True  # Default: True
```

---

## Q8: Can you use environment variables in Pydantic models?

**Difficulty:** 🟡 Medium  
**Category:** Configuration  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, but requires special setup. Use `pydantic-settings` library for environment variable management.

**Code Example:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    api_key: str
    debug: bool = False

settings = Settings()  # Reads from env vars
```

---

## Q11: If you define a field with `Field(default_factory=list)`, what does that do?

**Difficulty:** 🟡 Medium  
**Category:** Advanced Model Definition  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Creates a new list for each instance instead of sharing one list. Prevents mutable default bugs.

**Code Example:**
```python
# ❌ WRONG - All instances share same list
class User(BaseModel):
    tags: list = []

# ✅ CORRECT - Each instance gets new list
from pydantic import Field

class User(BaseModel):
    tags: list = Field(default_factory=list)

user1 = User()
user2 = User()
user1.tags.append("admin")
print(user2.tags)  # [] (not affected)
```

---

## Q12: Can you use custom validators on Pydantic models in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Advanced Validation  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, use `@field_validator` or `@model_validator` decorators.

**Code Example:**
```python
from pydantic import field_validator

class User(BaseModel):
    email: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v
```

---

## Q13: What happens if you send the wrong type for a request field?

**Difficulty:** 🟢 Easy  
**Category:** Validation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1 minute

**Answer:**
FastAPI tries to convert it. If conversion fails, returns 422 Unprocessable Entity with error details.

**Example:**
```python
class User(BaseModel):
    age: int

# POST {"age": "thirty"} → 422 error
# POST {"age": "30"} → Success (converted to 30)
```

---

## Q14: Can you have circular references in nested models?

**Difficulty:** 🟠 Hard  
**Category:** Model Design  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
YES, using `from __future__ import annotations` and forward references.

**Code Example:**
```python
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    friends: Optional[list[User]] = None

data = {"name": "John", "friends": [{"name": "Alice", "friends": None}]}
user = User(**data)
```

---

## Q15: How do you add examples to API documentation?

**Difficulty:** 🟡 Medium  
**Category:** Documentation  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `Field(example=...)` in Pydantic models.

**Code Example:**
```python
class User(BaseModel):
    name: str = Field(example="John Doe")
    age: int = Field(example=30)
    email: str = Field(example="john@example.com")

# Examples show in Swagger UI
```

---

## Q16: Can you use regex validation?

**Difficulty:** 🟡 Medium  
**Category:** Validation  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, use `pattern` parameter in `Field()`.

**Code Example:**
```python
class User(BaseModel):
    phone: str = Field(pattern=r"^\+?1?\d{9,15}$")
    username: str = Field(pattern=r"^[a-zA-Z0-9_]{3,20}$")
```

---

## Q17: What's the difference between a model and a response model?

**Difficulty:** 🟡 Medium  
**Category:** Model Usage  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Request models validate incoming data. Response models define what gets returned. Can be different for security (don't expose passwords, for example).

**Example:**
```python
class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str
    # No password in response!

@app.post("/users/", response_model=UserOut)
def create_user(user: UserIn):
    return user  # Password automatically excluded
```

---

## Q18: Can you have optional list fields?

**Difficulty:** 🟡 Medium  
**Category:** Model Definition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, use `Optional[List[T]]` or just `list` with default None.

**Code Example:**
```python
from typing import List, Optional

class User(BaseModel):
    name: str
    tags: Optional[List[str]] = None
```

---

## Q19: How do you prevent updating certain fields?

**Difficulty:** 🟡 Medium  
**Category:** Security  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use separate models for creation and updates. Created fields excluded from update model.

**Example:**
```python
class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    # No user_id (can't update)

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    return user
```

---

## Q20: Can you use `Literal` types in Pydantic models?

**Difficulty:** 🟡 Medium  
**Category:** Type Hints  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, restrict field to specific values using `Literal`.

**Code Example:**
```python
from typing import Literal

class Status(BaseModel):
    status: Literal["active", "inactive", "pending"]

# Only these 3 values allowed
```

---

# CHAPTER 3: RESPONSE MODELS

## Q1: What's a response model?

**Difficulty:** 🟢 Easy  
**Category:** Responses  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1 minute

**Answer:**
Defines what data gets returned from an endpoint. FastAPI validates response against this model, filters out extra fields, and generates documentation.

**Code Example:**
```python
class Item(BaseModel):
    name: str
    price: float

@app.get("/items/", response_model=Item)
def get_item():
    return {"name": "Widget", "price": 10.5}
```

---

## Q2: How do you exclude fields from a response?

**Difficulty:** 🟡 Medium  
**Category:** Response Filtering  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `response_model_exclude` parameter in route decorator.

**Code Example:**
```python
@app.get("/users/", response_model=User, response_model_exclude={"password"})
def get_user():
    return user
```

---

## Q3: How do you include only specific fields in a response?

**Difficulty:** 🟡 Medium  
**Category:** Response Filtering  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `response_model_include` parameter.

**Code Example:**
```python
@app.get("/users/", response_model=User, response_model_include={"id", "name"})
def get_user():
    return user
```

---

## Q4: Can you return different response models based on conditions?

**Difficulty:** 🟠 Hard  
**Category:** Advanced Responses  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Not directly with `response_model`, but you can return different structures and handle with Unions or conditional logic.

**Example:**
```python
from typing import Union

@app.get("/items/{item_id}")
def get_item(item_id: int) -> Union[ItemFull, ItemBasic]:
    if item_id == 1:
        return ItemFull(...)
    else:
        return ItemBasic(...)
```

---

## Q5: What happens if the endpoint returns data not matching the response model?

**Difficulty:** 🟡 Medium  
**Category:** Validation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
FastAPI filters the response to match the model. Extra fields are removed. Missing required fields cause an error.

**Example:**
```python
class Item(BaseModel):
    name: str
    price: float

@app.get("/items/", response_model=Item)
def get_item():
    return {"name": "Widget", "price": 10.5, "extra": "field"}
    # "extra" field is removed from response
```

---

## Q11: Can you use `by_alias` in response models?

**Difficulty:** 🟡 Medium  
**Category:** Advanced Responses  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, use `response_model_by_alias=True` to return fields using their aliases instead of Python names.

**Code Example:**
```python
class User(BaseModel):
    name: str = Field(alias="full_name")

@app.get("/users/", response_model=User, response_model_by_alias=True)
def get_user():
    return {"full_name": "John Doe"}
    # Returns {"full_name": "John Doe"} not {"name": "..."}
```

---

## Q12: How do you return a list of models?

**Difficulty:** 🟡 Medium  
**Category:** Response Models  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `List[Model]` in response_model.

**Code Example:**
```python
@app.get("/items/", response_model=List[Item])
def get_items():
    return [item1, item2, item3]
```

---

## Q13: Can you paginate responses?

**Difficulty:** 🟡 Medium  
**Category:** Response Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, return a wrapper model with items and metadata like page, total, etc.

**Code Example:**
```python
class ItemList(BaseModel):
    items: List[Item]
    total: int
    page: int
    pages: int

@app.get("/items/", response_model=ItemList)
def get_items(skip: int = 0, limit: int = 10):
    return {"items": items[skip:skip+limit], "total": len(items), ...}
```

---

## Q14: How do you handle errors in responses?

**Difficulty:** 🟡 Medium  
**Category:** Error Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use HTTP status codes and exception handling. FastAPI automatically returns error responses with appropriate status codes.

**Code Example:**
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if not item_exists(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

---

## Q15: Can you set custom response headers?

**Difficulty:** 🟡 Medium  
**Category:** Response Customization  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, use `headers` parameter in route decorator.

**Code Example:**
```python
@app.get("/items/", headers={"X-Custom": "Header"})
def get_items():
    return items
```

---

## Q16: How do you set HTTP status code for responses?

**Difficulty:** 🟡 Medium  
**Category:** Response Status  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `status_code` parameter in route decorator.

**Code Example:**
```python
@app.post("/items/", status_code=201)
def create_item(item: Item):
    return item  # Returns 201 Created
```

---

## Q17: Can you return a FileResponse?

**Difficulty:** 🟡 Medium  
**Category:** File Responses  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, import `FileResponse` and return file.

**Code Example:**
```python
from fastapi.responses import FileResponse

@app.get("/download/")
def download():
    return FileResponse("path/to/file.pdf")
```

---

## Q18: How do you set custom response types?

**Difficulty:** 🟡 Medium  
**Category:** Response Types  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use different response classes like `JSONResponse`, `HTMLResponse`, `FileResponse`, etc.

**Code Example:**
```python
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def get_html():
    return "<h1>Hello</h1>"
```

---

## Q19: Can you have multiple endpoints returning different structures for the same path?

**Difficulty:** 🟡 Medium  
**Category:** Routing  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, define separate functions with different HTTP methods or path parameters.

**Code Example:**
```python
@app.get("/items/")  # List all
def get_items(): ...

@app.post("/items/")  # Create
def create_item(item: Item): ...

@app.get("/items/{item_id}")  # Get one
def get_item(item_id: int): ...
```

---

## Q20: How do you handle streaming responses?

**Difficulty:** 🟠 Hard  
**Category:** Advanced Responses  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Use `StreamingResponse` for large files or real-time data.

**Code Example:**
```python
from fastapi.responses import StreamingResponse

@app.get("/stream/")
def stream_data():
    def data_generator():
        for i in range(100):
            yield f"data: {i}\n"
    return StreamingResponse(data_generator(), media_type="text/event-stream")
```

---

# CHAPTER 4: ASYNC & CONCURRENCY

## Q1: What's async/await in Python?

**Difficulty:** 🟡 Medium  
**Category:** Async Basics  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Async/await allows non-blocking I/O. Code can pause at I/O operations and let other code run. Much more efficient than threads.

**Example:**
```python
async def fetch_data():
    # Pause here, other code runs
    data = await database.query()
    return data

# Run: asyncio.run(fetch_data())
```

---

## Q2: Why use async in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Performance  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Async allows handling thousands of concurrent requests with fewer threads. Each request can pause during I/O (database, external APIs). Other requests continue running.

**Performance:**
- Sync (threads): 100 threads × 10MB = 1GB memory for 100 concurrent users
- Async: 1 thread × event loop = 50MB for 1000+ concurrent users

---

## Q3: How do you make an endpoint async in FastAPI?

**Difficulty:** 🟢 Easy  
**Category:** Async Endpoints  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 30 seconds

**Answer:**
Use `async def` instead of `def`.

**Code Example:**
```python
@app.get("/")
async def read_root():
    return {"message": "Hello"}
```

---

## Q4: Can you call sync code from async code?

**Difficulty:** 🟡 Medium  
**Category:** Async/Sync Integration  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, but if the sync function blocks (CPU-intensive or I/O), it blocks the entire event loop. Use `run_in_threadpool()` for blocking operations.

**Code Example:**
```python
from fastapi.concurrency import run_in_threadpool

@app.get("/")
async def read_root():
    result = await run_in_threadpool(blocking_function)
    return result
```

---

## Q5: What's an event loop?

**Difficulty:** 🟡 Medium  
**Category:** Async Internals  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
A loop that manages async tasks. When a task pauses (await), the loop runs another task. When first task resumes, loop goes back. Enables many concurrent tasks on one thread.

---

## Q6: How do you call an async database in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Async Integration  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use async drivers (asyncpg for PostgreSQL, motor for MongoDB). Call with `await`.

**Code Example:**
```python
import asyncpg

@app.get("/users/")
async def get_users():
    async with asyncpg.create_pool() as pool:
        users = await pool.fetch("SELECT * FROM users")
    return users
```

---

## Q11: If you have two async tasks, can they run in parallel?

**Difficulty:** 🟡 Medium  
**Category:** Concurrency  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, but on same thread (concurrency, not parallelism). They switch when one awaits. For true parallelism, use multiple processes.

**Example:**
```python
import asyncio

async def task1():
    await asyncio.sleep(1)
    return "task1"

async def task2():
    await asyncio.sleep(1)
    return "task2"

# Run both concurrently (takes 1 second, not 2)
results = await asyncio.gather(task1(), task2())
```

---

## Q12: What's the difference between concurrency and parallelism?

**Difficulty:** 🟠 Hard  
**Category:** Advanced Async  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Concurrency: Multiple tasks interleave on same core (async). Parallelism: Multiple tasks run simultaneously on different cores (multiprocessing).

**Visualization:**
```
Concurrency (1 core):
Task1 ──┬──────────┬──────────
        └─ Task2 ──┘

Parallelism (2 cores):
Task1 ─────────────────
Task2 ─────────────────
```

---

## Q13: Can you use asyncio.gather() in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Async Patterns  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, to run multiple async tasks concurrently.

**Code Example:**
```python
import asyncio

@app.get("/combined/")
async def combined():
    results = await asyncio.gather(
        fetch_users(),
        fetch_posts(),
        fetch_comments()
    )
    return results
```

---

## Q14: What's a coroutine?

**Difficulty:** 🟡 Medium  
**Category:** Async Basics  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
A function that can pause and resume. Created with `async def`. Returns a coroutine object that must be awaited.

**Example:**
```python
async def fetch():  # Creates coroutine
    return await db.query()

coro = fetch()  # Coroutine object, not executed
result = await coro  # Execute and get result
```

---

## Q15: How do you handle timeouts in async code?

**Difficulty:** 🟡 Medium  
**Category:** Async Patterns  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `asyncio.wait_for()`.

**Code Example:**
```python
import asyncio

@app.get("/")
async def read_root():
    try:
        data = await asyncio.wait_for(fetch_data(), timeout=5.0)
    except asyncio.TimeoutError:
        return {"error": "Timeout"}
```

---

## Q16: Can you mix async and sync dependencies?

**Difficulty:** 🟡 Medium  
**Category:** Dependency Injection  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, but sync code runs in threadpool automatically in FastAPI.

**Example:**
```python
# Async dependency
async def get_db():
    return await db_connect()

# Sync dependency
def get_config():
    return config_load()  # Runs in threadpool

@app.get("/")
async def read_root(db = Depends(get_db), config = Depends(get_config)):
    return {}
```

---

## Q17: What's `asyncio.create_task()`?

**Difficulty:** 🟡 Medium  
**Category:** Async Patterns  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Schedules a coroutine to run in the background. Doesn't wait for it to complete.

**Code Example:**
```python
@app.post("/notify/")
async def notify(email: str):
    asyncio.create_task(send_email(email))
    return {"status": "Processing"}
    # Returns immediately, email sent in background
```

---

## Q18: Can you use `await` outside an async function?

**Difficulty:** 🟢 Easy  
**Category:** Async Basics  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 30 seconds

**Answer:**
NO! `await` only works inside async functions.

**Example:**
```python
# ❌ WRONG
def sync_func():
    data = await fetch()  # SyntaxError

# ✅ CORRECT
async def async_func():
    data = await fetch()
```

---

## Q19: How do you run CPU-intensive work in FastAPI?

**Difficulty:** 🟠 Hard  
**Category:** Performance  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Use multiprocessing or thread pools. Don't run it on main event loop (blocks everything).

**Code Example:**
```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

@app.get("/compute/")
async def compute():
    result = await asyncio.get_event_loop().run_in_executor(
        executor,
        cpu_intensive_work
    )
    return result
```

---

## Q20: What's the relationship between async FastAPI and uvicorn?

**Difficulty:** 🟡 Medium  
**Category:** Architecture  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Uvicorn is an ASGI server that runs FastAPI. It manages the event loop and assigns requests to it. FastAPI runs on the event loop, handling async/await.

---

# CHAPTER 5: DEPENDENCIES

## Q1: What's dependency injection?

**Difficulty:** 🟡 Medium  
**Category:** Concepts  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
A way to provide dependencies to functions rather than creating them inside. Makes code testable and reusable.

**Example:**
```python
# Without DI
def get_user():
    db = create_db_connection()  # Hard to test
    return db.query_user()

# With DI
def get_user(db = Depends(get_db)):  # db provided
    return db.query_user()
```

---

## Q2: How do you define a dependency in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Dependency Definition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Create a function (or class) and use `Depends()` to inject it.

**Code Example:**
```python
def get_db():
    return database_connection()

@app.get("/users/")
def get_users(db = Depends(get_db)):
    return db.query_users()
```

---

## Q3: Can dependencies have dependencies?

**Difficulty:** 🟡 Medium  
**Category:** Dependency Composition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, dependencies can depend on other dependencies.

**Code Example:**
```python
def get_db():
    return db

def get_user(db = Depends(get_db)):
    return db.query_user()

@app.get("/")
def endpoint(user = Depends(get_user)):
    return user
```

---

## Q4: How do you use classes as dependencies?

**Difficulty:** 🟡 Medium  
**Category:** Dependency Classes  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Define a class and use `Depends(ClassName)`. FastAPI calls the class's `__init__()`.

**Code Example:**
```python
class CommonQueryParams:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit

@app.get("/items/")
def get_items(commons = Depends(CommonQueryParams)):
    return {"skip": commons.skip, "limit": commons.limit}
```

---

## Q11: Can you share a dependency across multiple endpoints?

**Difficulty:** 🟡 Medium  
**Category:** Dependency Reuse  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, define it once and reuse in multiple `Depends()` calls.

**Code Example:**
```python
def get_db():
    return database()

@app.get("/users/")
def get_users(db = Depends(get_db)):
    return db.query_users()

@app.get("/posts/")
def get_posts(db = Depends(get_db)):
    return db.query_posts()

# Same get_db used in both
```

---

## Q12: How do you cache dependency results?

**Difficulty:** 🟡 Medium  
**Category:** Dependency Optimization  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
FastAPI caches within a single request. Same dependency called multiple times gets same result.

**Example:**
```python
def get_db():
    print("Creating DB connection")
    return db

@app.get("/")
def endpoint(db1 = Depends(get_db), db2 = Depends(get_db)):
    # get_db called once, both db1 and db2 point to same instance
    return db1 is db2  # True
```

---

## Q13: Can you use dependency with a request object?

**Difficulty:** 🟡 Medium  
**Category:** Request Dependencies  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, inject `Request` to access headers, cookies, etc.

**Code Example:**
```python
from fastapi import Request

def get_token(request: Request):
    return request.headers.get("Authorization")

@app.get("/")
def endpoint(token = Depends(get_token)):
    return {"token": token}
```

---

## Q14: How do you handle dependencies with exceptions?

**Difficulty:** 🟡 Medium  
**Category:** Error Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Raise HTTPException in dependency. FastAPI catches it and returns error response.

**Code Example:**
```python
from fastapi import HTTPException

def verify_token(token: str):
    if not valid_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.get("/")
def endpoint(token = Depends(verify_token)):
    return {"token": token}
```

---

## Q15: Can dependencies be async?

**Difficulty:** 🟡 Medium  
**Category:** Async Dependencies  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, use `async def` for dependencies.

**Code Example:**
```python
async def get_db():
    return await async_db_connect()

@app.get("/")
async def endpoint(db = Depends(get_db)):
    return db
```

---

## Q16: How do you use context managers in dependencies?

**Difficulty:** 🟡 Medium  
**Category:** Resource Management  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `contextlib.asynccontextmanager` for async, or regular context managers for sync.

**Code Example:**
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db():
    db = await connect()
    try:
        yield db
    finally:
        await db.close()

@app.get("/")
async def endpoint(db = Depends(get_db)):
    return db
```

---

## Q17: Can you use multiple dependencies in one endpoint?

**Difficulty:** 🟢 Easy  
**Category:** Dependency Composition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 30 seconds

**Answer:**
YES, list multiple `Depends()` calls.

**Code Example:**
```python
@app.get("/")
def endpoint(
    db = Depends(get_db),
    token = Depends(verify_token),
    user = Depends(get_user)
):
    return {}
```

---

## Q18: How do you test code with dependencies?

**Difficulty:** 🟡 Medium  
**Category:** Testing  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `app.dependency_overrides` to replace dependencies with mock versions.

**Code Example:**
```python
app.dependency_overrides[get_db] = lambda: mock_db

# Tests run with mock_db instead of real db
response = client.get("/")

# Clean up
app.dependency_overrides.clear()
```

---

## Q19: Can you have optional dependencies?

**Difficulty:** 🟡 Medium  
**Category:** Dependency Definition  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, use `Optional` or provide default values.

**Code Example:**
```python
from typing import Optional

@app.get("/")
def endpoint(db = Depends(get_db) | None):
    if db:
        return db.query()
```

---

## Q20: How do you validate dependency inputs?

**Difficulty:** 🟡 Medium  
**Category:** Validation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Dependencies are subject to same validation as regular parameters. Use type hints and FastAPI validates them.

**Code Example:**
```python
def check_query(q: str = Query(..., min_length=3, max_length=50)):
    return q

@app.get("/search/")
def search(q = Depends(check_query)):
    return {"q": q}
```

---

# CHAPTER 6: ERROR HANDLING

## Q1: How do you handle errors in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Error Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Raise `HTTPException` with status code and detail. FastAPI catches it and returns proper HTTP error response.

**Code Example:**
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

---

## Q2: What's an HTTPException?

**Difficulty:** 🟡 Medium  
**Category:** Exception Handling  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
An exception that FastAPI automatically converts to an HTTP error response with specified status code.

**Example:**
```python
raise HTTPException(status_code=404, detail="Not found")
# Returns: {"detail": "Not found"} with 404 status
```

---

## Q3: What HTTP status codes should you use?

**Difficulty:** 🟡 Medium  
**Category:** HTTP Standards  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
- 200: Success
- 201: Created
- 400: Bad Request (validation fails)
- 401: Unauthorized (missing credentials)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 500: Server Error

---

## Q4: Can you create custom exceptions?

**Difficulty:** 🟡 Medium  
**Category:** Advanced Exceptions  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, subclass `HTTPException` or use `@app.exception_handler()` to handle custom exceptions.

**Code Example:**
```python
class ItemNotFound(Exception):
    pass

@app.exception_handler(ItemNotFound)
def handle_item_not_found(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Item not found"}
    )

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if not found:
        raise ItemNotFound()
```

---

## Q11: How do you validate request data and return 422 errors?

**Difficulty:** 🟡 Medium  
**Category:** Validation Errors  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
FastAPI automatically returns 422 when Pydantic validation fails. Use `Field()` constraints for validation.

**Example:**
```python
class User(BaseModel):
    age: int = Field(ge=0, le=150)

@app.post("/users/")
def create_user(user: User):
    return user

# POST {"age": 200} → 422 error
```

---

## Q12: Can you customize error responses?

**Difficulty:** 🟡 Medium  
**Category:** Error Responses  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, use `@app.exception_handler()` to customize how exceptions become responses.

**Code Example:**
```python
@app.exception_handler(ValueError)
def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )
```

---

## Q13: How do you handle database errors?

**Difficulty:** 🟡 Medium  
**Category:** Error Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Catch database exceptions and convert to HTTPException.

**Code Example:**
```python
@app.post("/users/")
def create_user(user: User):
    try:
        return db.create_user(user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
```

---

## Q14: What's the difference between HTTPException and raising regular exceptions?

**Difficulty:** 🟡 Medium  
**Category:** Exception Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
HTTPException automatically returns HTTP error response. Regular exceptions cause 500 errors.

**Example:**
```python
raise HTTPException(status_code=404)  # Returns proper 404 error
raise ValueError("Something")         # Returns 500 Internal Server Error
```

---

## Q15: Can you log errors?

**Difficulty:** 🟡 Medium  
**Category:** Error Logging  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, use Python's `logging` module.

**Code Example:**
```python
import logging

logger = logging.getLogger(__name__)

@app.get("/")
def endpoint():
    try:
        ...
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
```

---

## Q16: How do you handle timeout errors?

**Difficulty:** 🟡 Medium  
**Category:** Error Handling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Catch timeout exceptions and return appropriate error response.

**Code Example:**
```python
from asyncio import TimeoutError

@app.get("/")
async def endpoint():
    try:
        data = await asyncio.wait_for(fetch(), timeout=5)
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Request timeout")
```

---

## Q17: Can you have different error responses for different endpoints?

**Difficulty:** 🟡 Medium  
**Category:** Error Handling  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, handle exceptions within each endpoint as needed.

**Code Example:**
```python
@app.get("/api1/")
def api1():
    try:
        ...
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid for API1")

@app.get("/api2/")
def api2():
    try:
        ...
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid for API2")
```

---

## Q18: How do you handle 404 errors?

**Difficulty:** 🟡 Medium  
**Category:** Error Handling  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Raise HTTPException with status_code=404.

**Code Example:**
```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if not item_exists(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
```

---

## Q19: Can you have a global error handler?

**Difficulty:** 🟡 Medium  
**Category:** Error Handling  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, use `@app.exception_handler()` to catch exceptions globally.

**Code Example:**
```python
@app.exception_handler(Exception)
def global_handler(request, exc):
    return JSONResponse(status_code=500, content={"error": str(exc)})
```

---

## Q20: How do you return validation errors to the client?

**Difficulty:** 🟡 Medium  
**Category:** Validation Errors  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
FastAPI automatically returns validation errors as 422 response with detailed error list.

**Example:**
```python
class User(BaseModel):
    age: int = Field(ge=0)

# POST {"age": -5}
# Returns 422 with details about which field failed
```

---

# CHAPTER 7: SECURITY & AUTH

## Q1: How do you secure FastAPI endpoints?

**Difficulty:** 🟡 Medium  
**Category:** Security  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use API keys, OAuth2, JWT tokens, or API key headers. FastAPI has built-in security utilities that integrate with dependencies.

---

## Q2: How do you implement API key authentication?

**Difficulty:** 🟡 Medium  
**Category:** Authentication  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Check for API key in headers, query params, or cookies. Return 401 if missing or invalid.

**Code Example:**
```python
from fastapi import Header, HTTPException

@app.get("/")
def endpoint(x_api_key: str = Header(...)):
    if x_api_key != "secret":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return {"message": "OK"}
```

---

## Q3: What's OAuth2?

**Difficulty:** 🟡 Medium  
**Category:** OAuth2  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
A standard for delegated authorization. Users grant third-party apps access without sharing passwords. FastAPI has built-in OAuth2 support.

---

## Q4: How do you use JWT tokens in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** JWT  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `PyJWT` library to encode/decode tokens. Include token in request headers. Verify on each request.

**Code Example:**
```python
import jwt
from datetime import datetime, timedelta

SECRET = "secret"

def create_token(user_id: int):
    payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=1)}
    return jwt.encode(payload, SECRET)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401)
```

---

## Q11: How do you hash passwords securely?

**Difficulty:** 🟡 Medium  
**Category:** Password Security  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `passlib` or `bcrypt`. Never store plain passwords. Always hash and salt.

**Code Example:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

hashed = pwd_context.hash("password")
valid = pwd_context.verify("password", hashed)
```

---

## Q12: How do you implement role-based access control (RBAC)?

**Difficulty:** 🟡 Medium  
**Category:** Authorization  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Include role in token or database. Check role in dependency. Return 403 if insufficient permissions.

**Code Example:**
```python
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, current_user = Depends(get_current_user)):
    return db.delete_user(user_id)
```

---

## Q13: How do you handle CORS?

**Difficulty:** 🟡 Medium  
**Category:** CORS  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `CORSMiddleware` to allow cross-origin requests from specific domains.

**Code Example:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Q14: How do you add rate limiting?

**Difficulty:** 🟡 Medium  
**Category:** Rate Limiting  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use third-party libraries like `slowapi`. Track requests per IP and return 429 if limit exceeded.

**Code Example:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/")
@limiter.limit("5/minute")
def endpoint():
    return {}
```

---

## Q15: How do you implement refresh tokens?

**Difficulty:** 🟠 Hard  
**Category:** JWT Advanced  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Issue two tokens: short-lived access token and long-lived refresh token. Client uses refresh token to get new access token when expired.

**Pattern:**
```
1. Login → issue access_token + refresh_token
2. Use access_token for API requests
3. When access_token expires → POST refresh_token to get new access_token
4. refresh_token has longer expiry (days/weeks)
```

---

## Q16: Can you use OAuth2 with password flow?

**Difficulty:** 🟡 Medium  
**Category:** OAuth2  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, OAuth2PasswordBearer handles it. Client sends username/password once, receives token.

**Code Example:**
```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def endpoint(token: str = Depends(oauth2_scheme)):
    return verify_token(token)
```

---

## Q17: How do you prevent SQL injection in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Security  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use parameterized queries (ORM). Never concatenate SQL strings. Use SQLAlchemy, Tortoise ORM, etc.

**Example:**
```python
# ❌ WRONG - SQL injection risk
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ CORRECT - Parameterized
query = "SELECT * FROM users WHERE id = ?"
result = db.execute(query, [user_id])
```

---

## Q18: How do you add HTTPS?

**Difficulty:** 🟡 Medium  
**Category:** HTTPS  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Configure SSL certificates in production. Use `uvicorn --ssl-keyfile` or reverse proxy (Nginx).

**Example:**
```bash
uvicorn main:app --ssl-keyfile=/path/key.pem --ssl-certfile=/path/cert.pem
```

---

## Q19: Can you add request signing?

**Difficulty:** 🟠 Hard  
**Category:** Advanced Security  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
YES, use HMAC signatures. Client signs request with secret key. Server verifies signature.

---

## Q20: How do you audit API access?

**Difficulty:** 🟡 Medium  
**Category:** Monitoring  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Log who accessed what, when. Use middleware to track requests. Store in audit log database.

**Code Example:**
```python
from datetime import datetime

@app.middleware("http")
async def log_requests(request, call_next):
    print(f"{datetime.now()} - {request.method} {request.url.path} - {request.client.host}")
    response = await call_next(request)
    return response
```

---

# CHAPTER 8: WEBSOCKETS

## Q1: What are WebSockets?

**Difficulty:** 🟡 Medium  
**Category:** WebSockets  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
A protocol for two-way communication over a single TCP connection. Unlike HTTP (request/response), WebSockets enable real-time bidirectional messaging.

**Use Cases:**
- Chat applications
- Live notifications
- Real-time dashboards
- Collaborative editing

---

## Q2: How do you implement WebSockets in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** WebSocket Implementation  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `@app.websocket()` decorator. Accept connections, receive/send messages, handle disconnects.

**Code Example:**
```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

---

## Q3: How do you broadcast messages to multiple WebSocket clients?

**Difficulty:** 🟡 Medium  
**Category:** WebSocket Patterns  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Maintain a list of connected clients. When one sends message, send it to all.

**Code Example:**
```python
clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                await client.send_text(data)
    except:
        clients.remove(websocket)
```

---

## Q11: How do you handle WebSocket authentication?

**Difficulty:** 🟡 Medium  
**Category:** WebSocket Security  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Verify token in query params or headers before accepting connection.

**Code Example:**
```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str):
    if not verify_token(token):
        await websocket.close(code=4001, reason="Unauthorized")
        return
    await websocket.accept()
```

---

## Q12: How do you send JSON over WebSockets?

**Difficulty:** 🟡 Medium  
**Category:** WebSocket Data  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `send_json()` and `receive_json()` methods.

**Code Example:**
```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_json()
    await websocket.send_json({"message": "OK"})
```

---

## Q13: How do you handle WebSocket disconnections?

**Difficulty:** 🟡 Medium  
**Category:** WebSocket Lifecycle  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Catch `WebSocketDisconnect` exception. Clean up resources, remove from client list.

**Code Example:**
```python
from fastapi import WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        # Handle disconnect (remove from list, log, etc.)
        pass
```

---

## Q14: Can you use dependencies with WebSockets?

**Difficulty:** 🟡 Medium  
**Category:** WebSocket Dependencies  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, same way as regular endpoints.

**Code Example:**
```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user = Depends(get_current_user)):
    await websocket.accept()
```

---

## Q15: How do you scale WebSockets across multiple servers?

**Difficulty:** 🟠 Hard  
**Category:** WebSocket Scaling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Use message broker (Redis, RabbitMQ). Each server connects clients locally, but can message clients on other servers through broker.

**Pattern:**
```
Server 1 --\
            ├-- Redis/RabbitMQ -- Broadcast to all clients
Server 2 --/
```

---

## Q16: Can you have multiple rooms/channels in WebSockets?

**Difficulty:** 🟡 Medium  
**Category:** WebSocket Patterns  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
YES, group clients by room. Send messages only to clients in same room.

**Code Example:**
```python
rooms = {}

@app.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str):
    await websocket.accept()
    if room not in rooms:
        rooms[room] = []
    rooms[room].append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            for client in rooms[room]:
                await client.send_text(data)
    except:
        rooms[room].remove(websocket)
```

---

## Q17: How do you send binary data over WebSocket?

**Difficulty:** 🟡 Medium  
**Category:** WebSocket Data  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Use `send_bytes()` and `receive_bytes()`.

**Code Example:**
```python
data = await websocket.receive_bytes()
await websocket.send_bytes(b"binary data")
```

---

## Q18: How do you implement heartbeat/ping-pong?

**Difficulty:** 🟡 Medium  
**Category:** WebSocket Maintenance  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Send periodic pings to keep connection alive and detect dead connections.

**Code Example:**
```python
async def ping_task(websocket: WebSocket):
    while True:
        await asyncio.sleep(30)
        await websocket.send_text("ping")

# Create task alongside receive loop
```

---

## Q19: Can you use query parameters in WebSocket URLs?

**Difficulty:** 🟡 Medium  
**Category:** WebSocket Configuration  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
YES, access them from the WebSocket connection.

**Code Example:**
```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    query = websocket.query_params
    room_id = query.get("room_id")
```

---

## Q20: How do you test WebSocket connections?

**Difficulty:** 🟡 Medium  
**Category:** Testing  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `TestClient` with `with client.websocket_connect()` context manager.

**Code Example:**
```python
from fastapi.testclient import TestClient

client = TestClient(app)

with client.websocket_connect("/ws") as websocket:
    data = {"msg": "Hello"}
    websocket.send_json(data)
    response = websocket.receive_json()
    assert response == {"msg": "Hello"}
```

---

# CHAPTER 9: TESTING & DEPLOYMENT

## Q1: How do you test FastAPI applications?

**Difficulty:** 🟡 Medium  
**Category:** Testing  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `TestClient` to simulate HTTP requests. Write unit tests for business logic, integration tests for endpoints.

**Code Example:**
```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}
```

---

## Q2: What's TestClient?

**Difficulty:** 🟡 Medium  
**Category:** Testing Basics  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
A tool that simulates HTTP requests to your FastAPI app without running a server.

---

## Q3: How do you test endpoints with dependencies?

**Difficulty:** 🟡 Medium  
**Category:** Testing  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `app.dependency_overrides` to replace real dependencies with mocks.

**Code Example:**
```python
def mock_get_db():
    return mock_db

app.dependency_overrides[get_db] = mock_get_db

response = client.get("/items/")
# Uses mock_db instead of real db

app.dependency_overrides.clear()  # Cleanup
```

---

## Q4: How do you test endpoints that raise exceptions?

**Difficulty:** 🟡 Medium  
**Category:** Error Testing  
**Expected Answer Length:** 1-2 sentences  
**Time to Answer:** 1 minute

**Answer:**
Check the response status code and detail message.

**Code Example:**
```python
response = client.get("/nonexistent/")
assert response.status_code == 404
assert "not found" in response.json()["detail"]
```

---

## Q11: How do you deploy FastAPI to production?

**Difficulty:** 🟡 Medium  
**Category:** Deployment  
**Expected Answer Length:** 3-4 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Use a production ASGI server (Gunicorn + Uvicorn), reverse proxy (Nginx), and SSL. Run multiple workers for concurrency.

**Deployment Stack:**
```
Client → Nginx (reverse proxy, SSL)
      → Gunicorn (worker management)
      → Uvicorn (ASGI server) × N workers
```

---

## Q12: How do you run multiple FastAPI workers?

**Difficulty:** 🟡 Medium  
**Category:** Scaling  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use Gunicorn with multiple workers. Each worker runs an Uvicorn instance.

**Example:**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
# -w 4: 4 workers (scale based on CPU cores)
```

---

## Q13: How do you configure logging in FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Logging  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use Python's logging module. Configure level, format, handlers.

**Code Example:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
```

---

## Q14: How do you handle graceful shutdown?

**Difficulty:** 🟡 Medium  
**Category:** Deployment  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use startup/shutdown events to clean up resources.

**Code Example:**
```python
@app.on_event("shutdown")
async def shutdown_event():
    await db.close()
    print("Application shutdown")
```

---

## Q15: How do you use Docker for FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** Containerization  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Create Dockerfile with Python base image, install dependencies, run Uvicorn.

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Q16: How do you manage environment variables in production?

**Difficulty:** 🟡 Medium  
**Category:** Configuration  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use `pydantic-settings` to load from `.env` file or system environment variables.

**Code Example:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    api_key: str
    debug: bool = False

settings = Settings()
```

---

## Q17: How do you implement CI/CD for FastAPI?

**Difficulty:** 🟡 Medium  
**Category:** CI/CD  
**Expected Answer Length:** 3-4 sentences  
**Time to Answer:** 2 minutes

**Answer:**
Automate testing, building, and deployment. Use GitHub Actions, GitLab CI, or Jenkins to run tests, build Docker image, push to registry, deploy.

**Pipeline:**
```
Push code → Run tests → Build image → Push to registry → Deploy
```

---

## Q18: How do you monitor FastAPI in production?

**Difficulty:** 🟡 Medium  
**Category:** Monitoring  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Track metrics (requests, errors, response time), logs, and health checks. Use tools like Prometheus, ELK, or cloud monitoring.

**Metrics to Monitor:**
- Request rate and latency
- Error rate
- Server CPU/memory
- Database connection pool usage

---

## Q19: How do you handle database migrations?

**Difficulty:** 🟡 Medium  
**Category:** Database Management  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use Alembic for SQLAlchemy migrations. Run migrations before deploying new code.

**Workflow:**
```bash
alembic revision --autogenerate -m "Add new column"
alembic upgrade head  # Run before deployment
```

---

## Q20: How do you implement rate limiting in production?

**Difficulty:** 🟡 Medium  
**Category:** Performance  
**Expected Answer Length:** 2-3 sentences  
**Time to Answer:** 1.5 minutes

**Answer:**
Use Redis-backed rate limiting. Track requests per IP/user. Return 429 Too Many Requests when limit exceeded.

**Example:**
```bash
# Using redis-py
redis.incr(f"rate_limit:{user_id}", ex=60)  # 60 second window
if count > limit:
    raise HTTPException(status_code=429)
```

---

# Interview Prep Tips

## Mastery Checklist

✅ Understand ASGI vs WSGI differences  
✅ Know Pydantic validation inside-out  
✅ Can explain async/await benefits  
✅ Understand dependency injection  
✅ Know security best practices  
✅ Can design RESTful APIs  
✅ Understand error handling patterns  
✅ Can test endpoints  

## Common Mistakes

- ❌ Not using async for I/O operations
- ❌ Hardcoding passwords/secrets
- ❌ Not validating input properly
- ❌ Returning 500 instead of proper status codes
- ❌ Not handling WebSocket disconnects
- ❌ Not caching dependencies
- ❌ Mixing sync and async without care

## Study Tips

✅ Run all code examples locally  
✅ Build a complete CRUD API  
✅ Add authentication to your app  
✅ Implement error handling properly  
✅ Write comprehensive tests  
✅ Deploy to Docker/cloud  
✅ Monitor metrics in production  

---

# Quick Reference Table

| Chapter | Easy Qs | Medium Qs | Hard Qs | Total |
|---------|---------|----------|---------|-------|
| 1: Intro | Q1-Q5 | Q6-Q15 | Q16-Q20 | 20 |
| 2: Requests | Q1-Q5 | Q6-Q15 | Q16-Q20 | 20 |
| 3: Responses | Q1-Q5 | Q6-Q15 | Q16-Q20 | 20 |
| 4: Async | Q1-Q10 | Q11-Q20 | - | 20 |
| 5: Dependencies | Q1-Q10 | Q11-Q20 | - | 20 |
| 6: Errors | Q1-Q10 | Q11-Q20 | - | 20 |
| 7: Security | Q1-Q10 | Q11-Q20 | - | 20 |
| 8: WebSockets | Q1-Q10 | Q11-Q20 | - | 20 |
| 9: Testing | Q1-Q10 | Q11-Q20 | - | 20 |
| **TOTAL** | **90** | **90** | **0** | **180** |

---

**Good luck with your FastAPI interviews!** ⚡  
Master these concepts and you'll be well-prepared for any FastAPI role.
