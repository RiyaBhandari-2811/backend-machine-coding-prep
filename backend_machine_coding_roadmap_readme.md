# Backend Machine-Coding Preparation: JavaScript, Java & Python

> **Goal:** Prepare for 30-minute backend machine-coding rounds covering
> REST API implementation and object-oriented design.\
> **Priority:** Python + FastAPI first, then JavaScript + Express, then
> Java + Spring Boot.\
> **Approach:** Learn concepts, implement them, test edge cases, explain
> trade-offs, and revisit the same problem in all three languages.

## How to use this checklist

-   [ ] Check a subtopic only when you can explain it and implement a
    small example without copying.
-   [ ] For every major concept, record one example, common mistakes,
    and interview questions in your notes.
-   [ ] Prioritize working implementations over passive video watching.
-   [ ] For the 7-day sprint, focus first on the **Core** items. Still
    use this complete roadmap as the long-term checklist.
-   [ ] Do not skip fundamentals just because time is short; learn the
    essentials quickly and practise them in code.

## 0. Interview workflow and problem-solving

-   [ ] 0.1 Read the problem carefully and restate the goal.
-   [ ] 0.2 Ask clarifying questions about inputs, outputs, constraints,
    and expected behavior.
-   [ ] 0.3 Identify entities, fields, relationships, and core
    operations.
-   [ ] 0.4 Identify happy paths, invalid inputs, and important edge
    cases.
-   [ ] 0.5 Choose in-memory storage or a database based on
    requirements.
-   [ ] 0.6 Choose a simple design that fits the time limit.
-   [ ] 0.7 Define API contracts or class responsibilities before
    coding.
-   [ ] 0.8 Implement the smallest working end-to-end path first.
-   [ ] 0.9 Test happy paths and failure paths.
-   [ ] 0.10 Explain complexity, trade-offs, and what you would improve
    with more time.
-   [ ] 0.11 Practise a 30-minute time budget: clarify, design,
    implement, test, explain.

## 1. Programming fundamentals shared across languages

### 1.1 Core programming concepts

-   [ ] 1.1.1 Variables, constants, assignment, and naming
-   [ ] 1.1.2 Primitive and reference types
-   [ ] 1.1.3 Type conversion and coercion
-   [ ] 1.1.4 Operators and expressions
-   [ ] 1.1.5 Conditional statements
-   [ ] 1.1.6 Loops and iteration
-   [ ] 1.1.7 Functions, parameters, return values, and scope
-   [ ] 1.1.8 Default arguments and optional values
-   [ ] 1.1.9 Collections: arrays/lists, maps/dictionaries, sets
-   [ ] 1.1.10 String manipulation and formatting
-   [ ] 1.1.11 Exceptions and error handling
-   [ ] 1.1.12 Modules, packages, imports, and project structure
-   [ ] 1.1.13 Reading environment variables and configuration
-   [ ] 1.1.14 Debugging with breakpoints, logs, and stack traces

### 1.2 Data structures and complexity for machine coding

-   [ ] 1.2.1 Array/list operations and their costs
-   [ ] 1.2.2 Hash maps/dictionaries for lookup by ID
-   [ ] 1.2.3 Sets for uniqueness and membership checks
-   [ ] 1.2.4 Queues and stacks
-   [ ] 1.2.5 Sorting, filtering, and searching collections
-   [ ] 1.2.6 Big-O time and space complexity
-   [ ] 1.2.7 Choosing data structures for CRUD and lookup problems

## 2. Python fundamentals

### 2.1 Syntax and everyday Python

-   [x] 2.1.1 Indentation and code blocks
-   [ ] 2.1.2 Variables, naming, and dynamic typing
-   [ ] 2.1.3 Numbers, strings, booleans, and `None`
-   [ ] 2.1.4 Operators and truthiness
-   [ ] 2.1.5 `if`, `elif`, `else`, `for`, and `while`
-   [ ] 2.1.6 Lists, tuples, sets, and dictionaries
-   [ ] 2.1.7 Slicing, comprehensions, and unpacking
-   [ ] 2.1.8 String methods and f-strings
-   [ ] 2.1.9 Functions, keyword arguments, and default arguments
-   [ ] 2.1.10 Mutable versus immutable objects
-   [ ] 2.1.11 `None`, identity, and equality
-   [ ] 2.1.12 Exceptions: `try`, `except`, `else`, `finally`, `raise`
-   [ ] 2.1.13 File and module imports
-   [ ] 2.1.14 Type hints: `str`, `int`, `bool`, `list`, `dict`,
    `Optional` / unions
-   [ ] 2.1.15 `dataclass` basics
-   [ ] 2.1.16 Classes, `self`, constructors, instance and class
    attributes
-   [ ] 2.1.17 Inheritance, composition, and polymorphism
-   [ ] 2.1.18 Virtual environments and dependency installation with
    `pip`
-   [ ] 2.1.19 `requirements.txt` or `pyproject.toml` basics
-   [ ] 2.1.20 Running a module and understanding tracebacks

### 2.2 Python concepts important for backend work

-   [ ] 2.2.1 `async` and `await`
-   [ ] 2.2.2 Synchronous versus asynchronous I/O
-   [ ] 2.2.3 Context managers and `with`
-   [ ] 2.2.4 Iterators and generators at a basic level
-   [ ] 2.2.5 Environment variables and settings
-   [ ] 2.2.6 Avoiding mutable default arguments
-   [ ] 2.2.7 Common Python mistakes and debugging

## 3. HTTP and REST API fundamentals

-   [ ] 3.1 Client-server model and request-response lifecycle
-   [ ] 3.2 HTTP methods: GET, POST, PUT, PATCH, DELETE
-   [ ] 3.3 Idempotency and safe methods
-   [ ] 3.4 URL paths, path parameters, and query parameters
-   [ ] 3.5 Headers, request bodies, and content types
-   [ ] 3.6 JSON serialization and deserialization
-   [ ] 3.7 Status codes: 200, 201, 204, 400, 401, 403, 404, 409, 422,
    429, 500
-   [ ] 3.8 REST resource naming and API consistency
-   [ ] 3.9 Request validation and response contracts
-   [ ] 3.10 Pagination, filtering, sorting, and search
-   [ ] 3.11 Error response design
-   [ ] 3.12 OpenAPI and interactive API documentation
-   [ ] 3.13 Timeouts, retries, and external API failure handling
-   [ ] 3.14 Basic CORS understanding

## 4. Python backend: FastAPI

### 4.1 Getting started

-   [ ] 4.1.1 Create a virtual environment and install FastAPI and
    Uvicorn
-   [ ] 4.1.2 Create the application and run the development server
-   [ ] 4.1.3 Understand the role of ASGI and Uvicorn at a high level
-   [ ] 4.1.4 Use `/docs` and `/redoc`
-   [ ] 4.1.5 Understand route decorators and endpoint functions

### 4.2 Routes, data, and validation

-   [ ] 4.2.1 GET, POST, PUT, PATCH, and DELETE endpoints
-   [ ] 4.2.2 Path parameters and query parameters
-   [ ] 4.2.3 Request bodies and Pydantic models
-   [ ] 4.2.4 Required fields, defaults, constraints, and field
    validation
-   [ ] 4.2.5 Separate create, update, and response schemas
-   [ ] 4.2.6 Response models and response serialization
-   [ ] 4.2.7 Status codes and response headers
-   [ ] 4.2.8 `HTTPException` and custom exception handlers
-   [ ] 4.2.9 Handling missing resources and invalid requests
-   [ ] 4.2.10 Returning lists, objects, and empty responses correctly

### 4.3 Structure and dependency injection

-   [ ] 4.3.1 Split routes with `APIRouter`
-   [ ] 4.3.2 Understand `Depends`
-   [ ] 4.3.3 Inject shared dependencies and configuration
-   [ ] 4.3.4 Separate router, service, and repository responsibilities
-   [ ] 4.3.5 Avoid putting all business logic in endpoint functions
-   [ ] 4.3.6 Use application startup/lifespan patterns appropriately
-   [ ] 4.3.7 Configure CORS when required

### 4.4 FastAPI asynchronous behavior

-   [ ] 4.4.1 `def` versus `async def`
-   [ ] 4.4.2 What `await` does
-   [ ] 4.4.3 Async-compatible versus blocking libraries
-   [ ] 4.4.4 Why CPU-heavy work is not automatically faster with async
-   [ ] 4.4.5 Concurrency basics and avoiding blocking the event loop

### 4.5 FastAPI testing

-   [ ] 4.5.1 Write endpoint tests with `pytest`
-   [ ] 4.5.2 Use FastAPI `TestClient`
-   [ ] 4.5.3 Test success and failure status codes
-   [ ] 4.5.4 Test validation errors and missing IDs
-   [ ] 4.5.5 Override dependencies in tests
-   [ ] 4.5.6 Keep tests repeatable and isolated

## 5. JavaScript backend: Node.js and Express

### 5.1 Node.js essentials

-   [ ] 5.1.1 Node.js runtime and npm
-   [ ] 5.1.2 Modules: CommonJS and ES modules
-   [ ] 5.1.3 `package.json`, scripts, and dependencies
-   [ ] 5.1.4 Objects, arrays, destructuring, and spread
-   [ ] 5.1.5 Promises, `async`, and `await`
-   [ ] 5.1.6 Event loop and non-blocking I/O at a high level
-   [ ] 5.1.7 `try/catch` and rejected promises
-   [ ] 5.1.8 Environment variables and configuration

### 5.2 Express API implementation

-   [ ] 5.2.1 Create an Express app and start the server
-   [ ] 5.2.2 Define routes for CRUD operations
-   [ ] 5.2.3 Read path parameters, query parameters, and JSON bodies
-   [ ] 5.2.4 Middleware and middleware order
-   [ ] 5.2.5 Request validation using a schema library
-   [ ] 5.2.6 Centralized error-handling middleware
-   [ ] 5.2.7 Async route error handling
-   [ ] 5.2.8 Separate routes, controllers, services, and repositories
-   [ ] 5.2.9 Return correct status codes and response bodies
-   [ ] 5.2.10 Test APIs with a test runner and HTTP testing library

## 6. Java backend: Core Java and Spring Boot

### 6.1 Core Java essentials

-   [ ] 6.1.1 Classes, objects, constructors, and access modifiers
-   [ ] 6.1.2 Interfaces, abstract classes, and inheritance
-   [ ] 6.1.3 Encapsulation, abstraction, polymorphism, and composition
-   [ ] 6.1.4 Collections: List, Set, Map, Queue
-   [ ] 6.1.5 Generics and `Optional`
-   [ ] 6.1.6 Exceptions: checked and unchecked
-   [ ] 6.1.7 Lambdas and streams at a practical level
-   [ ] 6.1.8 Maven or Gradle basics

### 6.2 Spring Boot API implementation

-   [ ] 6.2.1 Create and run a Spring Boot application
-   [ ] 6.2.2 `@RestController`, `@RequestMapping`, and HTTP method
    mappings
-   [ ] 6.2.3 `@PathVariable`, `@RequestParam`, and `@RequestBody`
-   [ ] 6.2.4 Dependency injection and constructor injection
-   [ ] 6.2.5 Controller, service, and repository layers
-   [ ] 6.2.6 DTOs and entity separation
-   [ ] 6.2.7 Bean Validation annotations
-   [ ] 6.2.8 `ResponseEntity` and status codes
-   [ ] 6.2.9 Centralized exception handling with `@ControllerAdvice`
-   [ ] 6.2.10 Spring Data JPA and repository basics
-   [ ] 6.2.11 Unit and web-layer testing with JUnit, Mockito, and
    MockMvc
-   [ ] 6.2.12 Basic configuration with profiles and environment
    variables

## 7. Database and persistence

### 7.1 SQL essentials

-   [ ] 7.1.1 Tables, rows, columns, primary keys, and foreign keys
-   [ ] 7.1.2 SELECT, INSERT, UPDATE, and DELETE
-   [ ] 7.1.3 WHERE, ORDER BY, LIMIT, and OFFSET
-   [ ] 7.1.4 Joins and relationships
-   [ ] 7.1.5 Unique constraints, nullability, and indexes
-   [ ] 7.1.6 Transactions and ACID basics
-   [ ] 7.1.7 Preventing duplicate or conflicting records

### 7.2 Integrating a database

-   [ ] 7.2.1 Decide when in-memory storage is sufficient
-   [ ] 7.2.2 Connect PostgreSQL or another relational database
-   [ ] 7.2.3 Understand ORM models and database schemas
-   [ ] 7.2.4 Create and update records through the ORM
-   [ ] 7.2.5 Handle sessions, connections, and cleanup
-   [ ] 7.2.6 Use migrations to version schema changes
-   [ ] 7.2.7 Understand transactions and rollback behavior
-   [ ] 7.2.8 Avoid N+1 queries and unnecessary database calls
-   [ ] 7.2.9 Use connection pooling at a basic level

### 7.3 Language-specific database tools

-   [ ] 7.3.1 Python: SQLAlchemy and Alembic basics
-   [ ] 7.3.2 JavaScript: a suitable SQL client or ORM
-   [ ] 7.3.3 Java: Spring Data JPA and Hibernate basics

## 8. Object-oriented design machine coding

### 8.1 Design fundamentals

-   [ ] 8.1.1 Identify entities, state, behavior, and relationships
-   [ ] 8.1.2 Encapsulation and invariants
-   [ ] 8.1.3 Abstraction and interfaces
-   [ ] 8.1.4 Inheritance versus composition
-   [ ] 8.1.5 Polymorphism and interchangeable implementations
-   [ ] 8.1.6 SOLID principles at a practical level
-   [ ] 8.1.7 Cohesion, coupling, and separation of concerns
-   [ ] 8.1.8 Use enums and value objects where appropriate
-   [ ] 8.1.9 Model state transitions and invalid operations
-   [ ] 8.1.10 Keep the design simple under a 30-minute time limit

### 8.2 Design patterns to recognize and use when appropriate

-   [ ] 8.2.1 Strategy
-   [ ] 8.2.2 Factory
-   [ ] 8.2.3 Observer
-   [ ] 8.2.4 State
-   [ ] 8.2.5 Builder
-   [ ] 8.2.6 Repository
-   [ ] 8.2.7 Avoid adding patterns without a real need

### 8.3 OOP machine-coding exercises

-   [ ] 8.3.1 Parking lot
-   [ ] 8.3.2 Library management
-   [ ] 8.3.3 Elevator system
-   [ ] 8.3.4 Movie or event seat booking
-   [ ] 8.3.5 Vending machine
-   [ ] 8.3.6 Splitwise-style expense sharing
-   [ ] 8.3.7 Rate limiter
-   [ ] 8.3.8 In-memory cache with expiry
-   [ ] 8.3.9 Implement at least one exercise in Python, JavaScript, and
    Java

## 9. API security and reliability

-   [ ] 9.1 Authentication versus authorization
-   [ ] 9.2 JWT basics and token validation
-   [ ] 9.3 Password hashing and safe credential handling
-   [ ] 9.4 Role-based and resource-level permissions
-   [ ] 9.5 Input validation and mass-assignment risks
-   [ ] 9.6 Secrets and configuration via environment or secret manager
-   [ ] 9.7 CORS and the difference between CORS and authentication
-   [ ] 9.8 CSRF basics and when browser cookie authentication matters
-   [ ] 9.9 Rate limiting and abuse prevention
-   [ ] 9.10 Timeouts, bounded retries, and exponential backoff
-   [ ] 9.11 Idempotency for retryable operations
-   [ ] 9.12 Avoid leaking secrets or internal errors in responses
-   [ ] 9.13 Validate authorization on every protected resource

## 10. Testing and code quality

-   [ ] 10.1 Unit tests for business logic
-   [ ] 10.2 API or integration tests
-   [ ] 10.3 Happy-path and negative-path testing
-   [ ] 10.4 Boundary conditions and malformed input
-   [ ] 10.5 Mock external dependencies where appropriate
-   [ ] 10.6 Test database behavior and transactions
-   [ ] 10.7 Linting and formatting
-   [ ] 10.8 Meaningful names, small functions, and readable code
-   [ ] 10.9 Reproduce and debug failures from stack traces
-   [ ] 10.10 Test the exact behavior required by the prompt

## 11. Production readiness and deployment

### 11.1 Packaging and configuration

-   [ ] 11.1.1 Keep secrets out of source control
-   [ ] 11.1.2 Separate development, test, and production configuration
-   [ ] 11.1.3 Pin and manage dependencies
-   [ ] 11.1.4 Add a useful README and setup instructions
-   [ ] 11.1.5 Add health and readiness endpoints when appropriate

### 11.2 Docker and CI/CD

-   [ ] 11.2.1 Write a Dockerfile
-   [ ] 11.2.2 Understand image, container, port, and environment
    variable
-   [ ] 11.2.3 Run the API and database locally with Docker Compose
-   [ ] 11.2.4 Build and run the container locally
-   [ ] 11.2.5 Create a CI pipeline that runs tests and linting
-   [ ] 11.2.6 Understand deployment configuration and database
    migrations
-   [ ] 11.2.7 Understand logs, failed deployments, and rollback basics
-   [ ] 11.2.8 Deploy one small service to a cloud platform

### 11.3 Observability

-   [ ] 11.3.1 Structured logs with useful context
-   [ ] 11.3.2 Request IDs or correlation IDs
-   [ ] 11.3.3 Latency, traffic, error rate, and saturation
-   [ ] 11.3.4 Metrics and basic tracing concepts
-   [ ] 11.3.5 Diagnose failures from logs and metrics

## 12. Performance and scalability fundamentals

-   [ ] 12.1 Measure before optimizing
-   [ ] 12.2 Understand latency versus throughput
-   [ ] 12.3 Profile code and identify bottlenecks
-   [ ] 12.4 Optimize database queries and add justified indexes
-   [ ] 12.5 Understand connection pools and resource limits
-   [ ] 12.6 Cache frequently requested data when appropriate
-   [ ] 12.7 Understand cache expiry and invalidation
-   [ ] 12.8 Use pagination instead of returning unbounded collections
-   [ ] 12.9 Understand concurrency and race conditions
-   [ ] 12.10 Understand worker processes and deployment concurrency
-   [ ] 12.11 Load-test a service and compare results before and after
    changes
-   [ ] 12.12 Avoid premature microservices and unnecessary
    infrastructure

## 13. GenAI backend essentials

> This section comes after the core backend and FastAPI foundations. The
> goal is to build APIs around AI services, not to master all of AI in
> this one-week sprint.

-   [ ] 13.1 Understand LLM, tokens, context windows, and model APIs
-   [ ] 13.2 Call an external LLM API securely from a backend
-   [ ] 13.3 Keep API keys on the server, never in frontend code
-   [ ] 13.4 Validate model inputs and outputs
-   [ ] 13.5 Handle timeouts, rate limits, retries, and provider errors
-   [ ] 13.6 Stream responses using Server-Sent Events (SSE)
-   [ ] 13.7 Understand when streaming improves user experience
-   [ ] 13.8 Understand embeddings and vector search at a high level
-   [ ] 13.9 Understand RAG request flow at a high level
-   [ ] 13.10 Design a simple document Q&A API as a follow-up project

## 14. Cross-language implementation practice

For each exercise, implement the same requirements in Python/FastAPI,
JavaScript/Express, and Java/Spring Boot.

-   [ ] 14.1 Task management CRUD API
-   [ ] 14.2 Employee directory with search and pagination
-   [ ] 14.3 Library book management API
-   [ ] 14.4 Appointment booking with conflict validation
-   [ ] 14.5 URL shortener
-   [ ] 14.6 API aggregation service calling an external API
-   [ ] 14.7 Authentication-protected resource API
-   [ ] 14.8 Implement a small rate limiter
-   [ ] 14.9 Compare validation, error handling, dependency injection,
    and testing
-   [ ] 14.10 Explain what is shared backend knowledge versus
    framework-specific knowledge

## 15. Seven-day focused sprint

This is the order for the immediate interview deadline. It prioritizes
essentials without pretending that production mastery can be completed
in a week.

### Day 1: Python essentials and first FastAPI API

-   [ ] 15.1 Python syntax, collections, functions, exceptions, classes,
    and type hints
-   [ ] 15.2 Virtual environment, dependencies, and running an
    application
-   [ ] 15.3 FastAPI routes, request bodies, Pydantic, and status codes
-   [ ] 15.4 Implement Task CRUD using in-memory storage
-   [ ] 15.5 Test success cases, missing IDs, and invalid inputs

### Day 2: FastAPI structure and persistence

-   [ ] 15.6 Routers, dependency injection, service layer, and error
    handling
-   [ ] 15.7 SQL and ORM fundamentals
-   [ ] 15.8 Connect a relational database if time permits
-   [ ] 15.9 Write basic tests with pytest and TestClient
-   [ ] 15.10 Explain `def` versus `async def`

### Day 3: OOP machine coding

-   [ ] 15.11 Practise requirement clarification and class
    identification
-   [ ] 15.12 Implement one OOP problem under a 30-minute limit
-   [ ] 15.13 Review composition, interfaces, SOLID basics, and edge
    cases
-   [ ] 15.14 Translate the design into Python if the first
    implementation used another language

### Day 4: JavaScript and Express

-   [ ] 15.15 Revise Node.js modules, Promises, async/await, and error
    handling
-   [ ] 15.16 Implement the same Task CRUD API in Express
-   [ ] 15.17 Add validation, middleware, and centralized errors
-   [ ] 15.18 Test the API under a 30-minute limit

### Day 5: Java and Spring Boot

-   [ ] 15.19 Revise classes, interfaces, collections, and exceptions
-   [ ] 15.20 Implement CRUD using controller, service, and repository
    layers
-   [ ] 15.21 Add DTOs, validation, and exception handling
-   [ ] 15.22 Practise explaining dependency injection

### Day 6: Mixed practice and backend essentials

-   [ ] 15.23 Solve one REST API challenge in 30 minutes
-   [ ] 15.24 Solve one OOP design challenge in 30 minutes
-   [ ] 15.25 Revise SQL, HTTP status codes, authentication, and error
    handling
-   [ ] 15.26 Review Docker and deployment fundamentals
-   [ ] 15.27 Practise one external API integration or async task

### Day 7: Mock interviews and revision

-   [ ] 15.28 Complete a Python/FastAPI mock round
-   [ ] 15.29 Complete a JavaScript or Java mock round
-   [ ] 15.30 Review missed requirements and edge cases
-   [ ] 15.31 Practise explaining design decisions and trade-offs
-   [ ] 15.32 Revisit weak topics instead of starting a large new topic

## 16. Definition of done for a 30-minute API exercise

-   [ ] I clarified ambiguous requirements.
-   [ ] I identified fields, operations, and constraints.
-   [ ] I chose a suitable storage strategy.
-   [ ] I implemented the core endpoints.
-   [ ] I used appropriate request validation and status codes.
-   [ ] I handled missing records and invalid input.
-   [ ] I tested the main success and failure paths.
-   [ ] I kept the code readable and reasonably separated.
-   [ ] I explained what I would improve with more time.

## 17. Definition of done for an OOP exercise

-   [ ] I clarified the scope and core use cases.
-   [ ] I identified entities and their responsibilities.
-   [ ] I modelled state and enforced important invariants.
-   [ ] I used composition or interfaces where useful.
-   [ ] I avoided unnecessary classes and design patterns.
-   [ ] I implemented the primary use case end to end.
-   [ ] I tested edge cases and invalid state transitions.
-   [ ] I explained extension points and trade-offs.

## Progress log

Use this section to record daily progress.

  --------------------------------------------------------------------------
  Date           Topics studied Problems       What I         Next action
                                implemented    struggled with 
  -------------- -------------- -------------- -------------- --------------
  YYYY-MM-DD                                                  

  --------------------------------------------------------------------------

## Interview practice log

  ----------------------------------------------------------------------------
  Problem     Language         Time taken Completed?   Bugs /      Revisit?
                                                       missed      
                                                       cases       
  ----------- ------------ -------------- ------------ ----------- -----------
  Task CRUD   Python /                                             
  API         FastAPI                                              

  Task CRUD   JavaScript /                                         
  API         Express                                              

  Task CRUD   Java /                                               
  API         Spring Boot                                          

  OOP design                                                       
  ----------------------------------------------------------------------------

## Reference links

-   [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
-   [Python Tutorial](https://docs.python.org/3/tutorial/)
-   [Express Guide](https://expressjs.com/en/guide/routing.html)
-   [Spring Boot
    Reference](https://docs.spring.io/spring-boot/reference/)
-   [pytest Documentation](https://docs.pytest.org/)
-   [Docker Get Started](https://docs.docker.com/get-started/)

------------------------------------------------------------------------

**Working rule:** Understand the requirement, implement the smallest
correct solution, test it, then improve it. The checklist is
comprehensive; the seven-day sprint is the immediate priority.
Production-level mastery will continue beyond the sprint.
