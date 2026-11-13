# Chapter 2: HTTP Methods & CRUD Operations

## Table of Contents
1. [Introduction](#introduction)
2. [Static vs Dynamic Software](#static-vs-dynamic-software)
3. [Understanding CRUD Operations](#understanding-crud-operations)
4. [HTTP Methods Explained](#http-methods-explained)
5. [HTTP Methods in Web Applications](#http-methods-in-web-applications)
6. [Practical Examples](#practical-examples)
7. [HTTP Methods in FastAPI](#http-methods-in-fastapi)
8. [Common Mistakes & Best Practices](#common-mistakes--best-practices)
9. [Interview Questions & Answers](#interview-questions--answers)
10. [Summary](#summary)

---

## Introduction

When building APIs and web applications, understanding HTTP Methods is fundamental. HTTP Methods (also called HTTP Verbs) are the language through which clients communicate their intentions to servers. They tell the server: "What do you want me to do with this resource?"

In this chapter, we'll explore:
- Why HTTP Methods exist
- The four basic CRUD operations
- How HTTP Methods map to real-world interactions
- Practical implementation in FastAPI

---

## Static vs Dynamic Software

Before diving into HTTP Methods, let's understand the context where they're most important.

### Two Categories of Software

#### **Static Software**
Static software requires minimal user interaction. Users mainly retrieve information without modifying data.

**Characteristics:**
- One-way communication (from software to user)
- Limited interaction types
- Mainly for data consumption
- Examples: Calendar apps, Clock apps, News readers, Weather apps

**User Interaction:**
```
User: "Show me today's date"
Software: "Today is November 13, 2026"
(Interaction ends)
```

#### **Dynamic Software**
Dynamic software involves extensive user interaction where users can create, retrieve, update, and delete data.

**Characteristics:**
- Two-way communication (back-and-forth interaction)
- Multiple interaction types
- Users modify and manage data
- Examples: Microsoft Excel, Microsoft Word, Gmail, Instagram, Zomato, Facebook

**User Interaction:**
```
User: "Create a new spreadsheet"
Software: "Done! New spreadsheet created"
User: "Add data to cell A1"
Software: "Data saved"
User: "Delete row 5"
Software: "Row deleted"
```

### Why This Matters for APIs

When building APIs (which enable dynamic applications), you need a standardized way to express what operation the client wants to perform. This is where HTTP Methods come in.

---

## Understanding CRUD Operations

CRUD is the fundamental framework for all data operations in dynamic software. It stands for:

- **C**reate - Add new data/records
- **R**etrieve - Read/fetch existing data
- **U**pdate - Modify existing data
- **D**elete - Remove data

### Every Dynamic Software = CRUD

No matter what dynamic software you use, there are only **4 possible types of interactions**:

#### **1. CREATE**
Adding new data to the system.

**Real-world examples:**
- Instagram: Creating a new post
- Gmail: Composing a new email
- Zomato: Placing a new order
- Microsoft Excel: Creating a new cell or row
- **Your Project**: Creating a new patient record

#### **2. RETRIEVE**
Reading or fetching existing data without modifying it.

**Real-world examples:**
- Instagram: Scrolling through your feed, viewing someone's profile
- Gmail: Reading an existing email
- Zomato: Viewing past orders
- Microsoft Excel: Viewing cell values
- **Your Project**: Viewing all patients or a specific patient

#### **3. UPDATE**
Modifying existing data.

**Real-world examples:**
- Instagram: Editing a caption on your post
- Gmail: Editing a draft
- Zomato: Updating your delivery address
- Microsoft Excel: Changing a cell's value
- **Your Project**: Updating a patient's weight and recalculating BMI

#### **4. DELETE**
Removing data from the system.

**Real-world examples:**
- Instagram: Deleting a post or comment
- Gmail: Deleting an email
- Zomato: Removing a saved address
- Microsoft Excel: Deleting a row
- **Your Project**: Removing a patient record

### The Key Insight

**No matter how complex a software application is, every user interaction falls into one of these 4 categories.**

---

## HTTP Methods Explained

HTTP Methods are standardized verbs that indicate which CRUD operation you want to perform. They're part of the HTTP request sent from client to server.

### The Five Main HTTP Methods

#### **1. GET - Retrieve Data**

**Purpose:** Fetch data without modifying anything on the server

**CRUD Operation:** RETRIEVE

**Characteristics:**
- Safe (doesn't modify data)
- Idempotent (multiple calls produce same result)
- Cached by default
- Data passed in URL (no request body usually)
- Visible in browser history and logs

**When to use:**
- Fetching user profile
- Getting a list of items
- Retrieving search results
- Downloading files

**Example:**
```
GET http://api.example.com/patients
GET http://api.example.com/patients/5
GET http://api.example.com/patients?age=30
```

**Browser behavior:**
When you type a URL in your browser or click a link, it sends a GET request.

#### **2. POST - Create Data**

**Purpose:** Submit data to create a new resource

**CRUD Operation:** CREATE

**Characteristics:**
- Not idempotent (multiple calls may create duplicate resources)
- Data in request body (not visible in URL)
- Not cached by default
- Used when you need to submit sensitive data

**When to use:**
- User registration/signup
- Creating a new blog post
- Placing an order
- Uploading a file
- Submitting form data

**Example:**
```
POST http://api.example.com/patients
Body: {
  "name": "John Doe",
  "age": 30,
  "weight": 70
}
```

**Browser behavior:**
When you submit an HTML form with method="POST", it sends a POST request.

#### **3. PUT - Update Entire Resource**

**Purpose:** Update an existing resource with new data

**CRUD Operation:** UPDATE

**Characteristics:**
- Idempotent (multiple calls produce same result)
- Replaces entire resource
- Data in request body
- Requires resource ID

**When to use:**
- Updating a user profile completely
- Changing a patient's full record
- Replacing an entire document

**Example:**
```
PUT http://api.example.com/patients/5
Body: {
  "name": "John Smith",
  "age": 31,
  "weight": 72,
  "height": 180
}
```

#### **4. DELETE - Remove Resource**

**Purpose:** Remove a resource from the server

**CRUD Operation:** DELETE

**Characteristics:**
- Idempotent (deleting twice has same effect as once)
- Removes entire resource
- No request body typically

**When to use:**
- Deleting a user account
- Removing a blog post
- Canceling an order
- Removing a patient record

**Example:**
```
DELETE http://api.example.com/patients/5
```

#### **5. PATCH - Partial Update**

**Purpose:** Update only specific fields of a resource

**CRUD Operation:** UPDATE (partial)

**Characteristics:**
- Idempotent (usually)
- Partial update of resource
- Updates only specified fields
- Data in request body

**When to use:**
- Updating just a user's phone number
- Changing only a patient's weight (not entire record)
- Updating specific fields without full replacement

**Example:**
```
PATCH http://api.example.com/patients/5
Body: {
  "weight": 72
}
```

### Comparison: PUT vs PATCH

| Aspect | PUT | PATCH |
|--------|-----|-------|
| **Scope** | Full resource replacement | Partial update |
| **Fields** | All fields must be provided | Only changed fields needed |
| **Idempotent** | Yes | Usually yes |
| **Data Loss** | Missing fields deleted | Missing fields preserved |
| **Use Case** | Complete record replacement | Targeted updates |

**Example:**
```
Original Patient: { "id": 5, "name": "John", "age": 30, "weight": 70 }

PUT /patients/5 with { "age": 31 }
Result: { "id": 5, "age": 31 }  ❌ Other fields lost!

PATCH /patients/5 with { "age": 31 }
Result: { "id": 5, "name": "John", "age": 31, "weight": 70 }  ✅ Other fields preserved
```

### HTTP Method Frequency of Use

| Method | Frequency | Why |
|--------|-----------|-----|
| GET | Very High | Most data operations are reads |
| POST | High | Creating new resources is common |
| PUT | Medium | Full updates less common than partial |
| PATCH | Medium | Partial updates very practical |
| DELETE | Low | Deletions are less frequent |

---

## HTTP Methods in Web Applications

### How the Client-Server Communication Works

```
┌─────────────────┐                          ┌─────────────────┐
│     CLIENT      │                          │     SERVER      │
│   (Browser)     │                          │   (Web Server)  │
└────────┬────────┘                          └────────┬────────┘
         │                                           │
         │  1. User clicks a link                   │
         ├──────────GET /patients ─────────────────>│
         │                                           │
         │                                      2. Server processes
         │                                         request
         │                                           │
         │<─────────HTML response (Patient list)────┤
         │                                           │
         │  3. User fills form and submits           │
         ├──────────POST /patients ──────────────────>│
         │       (with patient data in body)        │
         │                                           │
         │                                      4. Server creates
         │                                         new patient
         │                                           │
         │<──────────Confirmation response──────────┤
         │                                           │
```

### Dynamic Websites Use All Methods

Consider Instagram:
- **GET**: Viewing feed, viewing profile, viewing comments
- **POST**: Creating a new post, writing a comment, liking
- **PUT**: Editing entire bio/profile
- **PATCH**: Changing just a caption
- **DELETE**: Removing a post, deleting a comment

Consider Zomato:
- **GET**: Viewing restaurants, viewing order history
- **POST**: Placing a new order
- **PATCH**: Updating delivery address
- **DELETE**: Canceling an order

### The Protocol: HTTP

All of this communication happens via **HTTP (HyperText Transfer Protocol)**.

**How it works:**
1. Client sends HTTP request with a method (GET, POST, etc.)
2. Server receives request and processes it
3. Server sends HTTP response
4. Communication ends (stateless)

---

## Practical Examples

### Example 1: Patient Management System

**Scenario:** Doctor using an app to manage patient records

```
CREATE (POST) - Doctor creates new patient
POST /api/patients
Body: {
  "name": "Rajesh Kumar",
  "age": 35,
  "height": 180,
  "weight": 75
}
Response: { "id": 10, "name": "Rajesh Kumar", ...}

RETRIEVE (GET) - View all patients
GET /api/patients
Response: [
  { "id": 1, "name": "Patient 1", ... },
  { "id": 2, "name": "Patient 2", ... },
  ...
]

RETRIEVE (GET) - View specific patient
GET /api/patients/10
Response: { "id": 10, "name": "Rajesh Kumar", ... }

UPDATE (PATCH) - Update patient's weight
PATCH /api/patients/10
Body: { "weight": 72 }
Response: { "id": 10, "name": "Rajesh Kumar", "weight": 72, ... }

DELETE (DELETE) - Remove patient
DELETE /api/patients/10
Response: { "message": "Patient deleted successfully" }
```

### Example 2: E-Commerce (Zomato)

```
CREATE (POST) - Place order
POST /api/orders
Body: { "restaurant_id": 5, "items": [...], "address": "..." }
Response: { "order_id": 123, ... }

RETRIEVE (GET) - Get order history
GET /api/users/42/orders
Response: [ { "order_id": 123, ... }, { "order_id": 124, ... } ]

RETRIEVE (GET) - Get order details
GET /api/orders/123
Response: { "order_id": 123, "status": "Delivered", ... }

UPDATE (PATCH) - Update delivery address
PATCH /api/orders/123
Body: { "delivery_address": "New Address" }
Response: { "order_id": 123, "delivery_address": "New Address" }

DELETE (DELETE) - Cancel order
DELETE /api/orders/123
Response: { "message": "Order cancelled" }
```

### Example 3: Social Media (Instagram)

```
CREATE (POST) - Create new post
POST /api/posts
Body: { "caption": "Beautiful sunset!", "image": "..." }
Response: { "post_id": 456, ... }

CREATE (POST) - Add comment
POST /api/posts/456/comments
Body: { "text": "Amazing photo!" }
Response: { "comment_id": 789, ... }

RETRIEVE (GET) - Get feed
GET /api/feed
Response: [ { "post_id": 456, ... }, { "post_id": 457, ... } ]

RETRIEVE (GET) - Get user profile
GET /api/users/12
Response: { "user_id": 12, "name": "John", ... }

UPDATE (PATCH) - Edit post caption
PATCH /api/posts/456
Body: { "caption": "Sunset at the beach" }
Response: { "post_id": 456, "caption": "Sunset at the beach" }

DELETE (DELETE) - Delete post
DELETE /api/posts/456
Response: { "message": "Post deleted" }
```

---

## HTTP Methods in FastAPI

### Defining Endpoints with Different Methods

```python
from fastapi import FastAPI

app = FastAPI()

# GET - Retrieve all patients
@app.get("/patients")
async def get_all_patients():
    return patients_list

# GET - Retrieve specific patient
@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    return get_patient_by_id(patient_id)

# POST - Create new patient
@app.post("/patients")
async def create_patient(patient: PatientModel):
    new_patient = save_patient(patient)
    return new_patient

# PATCH - Update patient (partial)
@app.patch("/patients/{patient_id}")
async def update_patient(patient_id: int, patient_update: PatientUpdate):
    updated_patient = partial_update(patient_id, patient_update)
    return updated_patient

# PUT - Replace entire patient record
@app.put("/patients/{patient_id}")
async def replace_patient(patient_id: int, patient: PatientModel):
    replaced_patient = full_replace(patient_id, patient)
    return replaced_patient

# DELETE - Remove patient
@app.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int):
    deleted_patient = remove_patient(patient_id)
    return {"message": "Patient deleted", "deleted": deleted_patient}
```

### Accessing These in Swagger UI

When you run your FastAPI app, visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

You'll see all endpoints grouped by HTTP Method with different colors:
- **GET** (Green) - Safe, read-only
- **POST** (Blue) - Create
- **PUT** (Orange) - Full update
- **PATCH** (Yellow) - Partial update
- **DELETE** (Red) - Delete

---

## Common Mistakes & Best Practices

### ❌ Common Mistakes

**1. Using GET for modifications**
```python
# WRONG
@app.get("/delete_patient/{patient_id}")
async def delete_patient(patient_id: int):
    return delete(patient_id)

# RIGHT
@app.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int):
    return delete(patient_id)
```

**2. Putting data in URL for POST**
```python
# WRONG
@app.post("/create_patient?name=John&age=30&weight=70")
async def create():
    pass

# RIGHT
@app.post("/patients")
async def create_patient(patient: PatientModel):
    pass
```

**3. Confusing PUT and PATCH**
```python
# PUT requires full resource
# PATCH requires partial update
```

**4. Using POST for everything**
- POST should be for creation, not all operations
- Use GET for retrieval, DELETE for removal, PATCH for updates

### ✅ Best Practices

**1. Use correct HTTP method for operation type**
- Data retrieval → GET
- Data creation → POST
- Data update → PATCH (partial) or PUT (full)
- Data deletion → DELETE

**2. Use meaningful URLs**
```python
# Good
@app.get("/patients")
@app.post("/patients")
@app.get("/patients/{patient_id}")
@app.patch("/patients/{patient_id}")
@app.delete("/patients/{patient_id}")

# Avoid
@app.get("/getpatients")
@app.post("/addpatients")
@app.get("/fetchpatient")
```

**3. Return appropriate HTTP status codes**
```python
from fastapi import status

@app.post("/patients", status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientModel):
    return created_patient

@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: int):
    delete(patient_id)
```

**4. Make operations idempotent when possible**
- GET: Always safe and idempotent
- DELETE: Multiple deletes should be safe (delete non-existent is OK)
- PUT: Replace entire resource (idempotent)
- PATCH: Usually idempotent
- POST: Not idempotent (may create duplicates)

---

## Interview Questions & Answers

### Q1: What are HTTP Methods and why do they exist?

**Answer:**
HTTP Methods are standardized verbs that indicate what operation a client wants to perform on a resource. They exist because:
- **Standardization**: Provides a universal way to communicate intent
- **Clarity**: Server understands exactly what client wants
- **Safety**: Methods can be marked as safe or unsafe
- **Caching**: Servers can cache GET requests but not POST
- **REST Architecture**: Foundation of RESTful API design

The main HTTP Methods are GET, POST, PUT, PATCH, and DELETE.

### Q2: What is CRUD and why is it important?

**Answer:**
CRUD stands for:
- **C**reate - Add new data
- **R**etrieve - Read existing data
- **U**pdate - Modify existing data
- **D**elete - Remove data

CRUD is important because:
- **Universal**: Every dynamic software performs these 4 operations
- **Simplified**: All user interactions fit into one of 4 categories
- **Framework**: Helps design APIs systematically
- **Predictability**: Users know what operations are available

### Q3: What's the difference between GET and POST?

**Answer:**

| Aspect | GET | POST |
|--------|-----|------|
| **Purpose** | Retrieve data | Create/Submit data |
| **CRUD Op** | Retrieve | Create |
| **Safe** | Yes | No |
| **Idempotent** | Yes | No |
| **Data Location** | URL query params | Request body |
| **Cached** | Yes | No |
| **Visibility** | Visible in URL | Hidden in body |
| **Use Case** | Fetching resources | Creating/Submitting forms |

**Key difference**: GET retrieves without modifying; POST submits data and may modify state.

### Q4: What's the difference between PUT and PATCH?

**Answer:**

**PUT (Full Update):**
```
Original: { "id": 1, "name": "John", "age": 30, "weight": 70 }

PUT /patients/1 with { "age": 31 }
Result: { "id": 1, "age": 31 }  ← Missing fields deleted!
```

**PATCH (Partial Update):**
```
Original: { "id": 1, "name": "John", "age": 30, "weight": 70 }

PATCH /patients/1 with { "age": 31 }
Result: { "id": 1, "name": "John", "age": 31, "weight": 70 }  ← Fields preserved
```

**Use PUT when**: Replacing entire resource
**Use PATCH when**: Updating specific fields

### Q5: Are DELETE requests idempotent?

**Answer:**
Yes, DELETE is idempotent. Calling DELETE multiple times has the same effect as calling it once.

```
DELETE /patients/5  → Deleted
DELETE /patients/5  → Already deleted (no error, idempotent)
DELETE /patients/5  → Still deleted (no error)
```

This is why it's safe to retry DELETE requests without worry about side effects.

### Q6: Why should you use correct HTTP methods?

**Answer:**
Using correct HTTP methods:

1. **Semantic Clarity**: Code is self-documenting
2. **Browser Support**: Browsers understand and handle methods appropriately
3. **Caching**: GET is cached automatically; POST is not
4. **Security**: POST hides data in body; GET is visible in URL
5. **API Standards**: RESTful APIs require correct method usage
6. **Developer Experience**: Other developers understand intent immediately
7. **HTTP Semantics**: Methods have defined behavior (idempotent, safe, etc.)

### Q7: How do HTTP methods map to database operations?

**Answer:**

| HTTP Method | CRUD | SQL | Database |
|-------------|------|-----|----------|
| GET | Retrieve | SELECT | Read data |
| POST | Create | INSERT | Add new row |
| PATCH | Update | UPDATE | Modify row(s) |
| PUT | Update (full) | UPDATE/REPLACE | Replace entire row |
| DELETE | Delete | DELETE | Remove row(s) |

### Q8: What happens if you use wrong HTTP method?

**Answer:**
While it might work (because HTTP doesn't enforce operations), it causes problems:

```python
# WRONG - Using GET to delete
@app.get("/delete_patient/{patient_id}")
async def delete_patient(patient_id: int):
    delete(patient_id)  # Works but wrong method!
    return {"deleted": True}
```

**Problems:**
- ❌ Violates REST standards
- ❌ Browser might cache GET request with delete operation
- ❌ Search engines might crawl and inadvertently delete data
- ❌ Other developers confused about intent
- ❌ API tools expect GET to be safe
- ❌ Fails security/API audits

### Q9: Can you change data with GET request?

**Answer:**
Technically yes, but you absolutely shouldn't.

```python
# WORKS but BAD PRACTICE
@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    patient = fetch_patient(patient_id)
    patient.visits += 1  # Modifying data
    save(patient)
    return patient
```

**Why it's bad:**
- GET should be **safe** (no side effects)
- GET requests are cached, so modification might not happen
- Browsers/proxies might retry GET requests
- Violates HTTP specifications
- Makes API unpredictable

### Q10: How do REST APIs use HTTP methods?

**Answer:**
RESTful APIs follow a pattern:

```
GET /resource              → List all resources
GET /resource/{id}         → Get specific resource
POST /resource             → Create new resource
PATCH /resource/{id}       → Partial update
PUT /resource/{id}         → Full replacement
DELETE /resource/{id}      → Delete resource
```

For Patient Management:
```
GET /patients              → List all patients
GET /patients/5            → Get patient #5
POST /patients             → Create new patient
PATCH /patients/5          → Update patient #5
DELETE /patients/5         → Delete patient #5
```

This consistency makes APIs intuitive and predictable.

### Q11: What is idempotency and which methods are idempotent?

**Answer:**
**Idempotency**: Calling an operation multiple times has the same effect as calling it once.

**Idempotent methods:**
- **GET**: Reading same data multiple times returns same result ✅
- **PUT**: Replacing with same data multiple times has same effect ✅
- **DELETE**: Deleting same resource multiple times has same effect ✅
- **PATCH**: Usually idempotent (depends on operation) ✅

**Non-idempotent:**
- **POST**: Creating multiple times creates multiple resources ❌

**Why it matters:**
- Servers can safely retry idempotent requests
- Network issues don't cause duplicate creation with idempotent methods
- Makes systems more robust

### Q12: What are HTTP status codes and why are they important?

**Answer:**
HTTP status codes indicate the result of a request:

**2xx - Success:**
- 200 OK - Request succeeded
- 201 Created - Resource created successfully
- 204 No Content - Success but no response body (DELETE)

**3xx - Redirect:**
- 301 Moved Permanently
- 302 Found

**4xx - Client Error:**
- 400 Bad Request - Invalid data
- 401 Unauthorized - Authentication required
- 404 Not Found - Resource doesn't exist
- 409 Conflict - Resource already exists (POST)

**5xx - Server Error:**
- 500 Internal Server Error
- 503 Service Unavailable

**Importance:**
```python
@app.post("/patients", status_code=201)
async def create_patient(patient: PatientModel):
    return created_patient  # 201 Created

@app.delete("/patients/{id}", status_code=204)
async def delete_patient(patient_id: int):
    delete(patient_id)  # 204 No Content
```

---

## Summary

- **HTTP Methods** are verbs indicating what operation to perform on a resource
- **CRUD** (Create, Retrieve, Update, Delete) represents all possible interactions with data
- **GET** retrieves data safely and idempotently
- **POST** creates new resources (not idempotent)
- **PUT** replaces entire resources (idempotent)
- **PATCH** partially updates resources (usually idempotent)
- **DELETE** removes resources (idempotent)
- **Static software** has minimal interaction; **dynamic software** has extensive CRUD operations
- Using correct HTTP methods is essential for **REST architecture**, **security**, **caching**, and **API standardization**
- **Idempotency** matters for reliability and retry logic
- **HTTP status codes** communicate operation results

In the next chapter, we'll implement all these HTTP methods in our Patient Management System API using FastAPI!

---

## Additional Resources

### HTTP Method Selection Flowchart

```
Do you want to...?

├─ Retrieve data → GET
├─ Create new resource → POST
├─ Update entire resource → PUT
├─ Update specific fields → PATCH
└─ Delete resource → DELETE
```

### Quick Reference Table

| Method | Purpose | CRUD | Idempotent | Cache | Body |
|--------|---------|------|-----------|-------|------|
| GET | Retrieve | R | ✅ | ✅ | ❌ |
| POST | Create | C | ❌ | ❌ | ✅ |
| PUT | Replace | U | ✅ | ❌ | ✅ |
| PATCH | Partial Update | U | ✅ | ❌ | ✅ |
| DELETE | Remove | D | ✅ | ❌ | ❌ |

### Common Endpoints Pattern

```
Resource: /patients

GET /patients                 → Get all patients
GET /patients/{id}           → Get specific patient
POST /patients               → Create new patient
PATCH /patients/{id}         → Update patient fields
PUT /patients/{id}           → Replace entire patient
DELETE /patients/{id}        → Delete patient
```

This pattern applies to ANY resource:
- /users, /posts, /orders, /products, etc.
