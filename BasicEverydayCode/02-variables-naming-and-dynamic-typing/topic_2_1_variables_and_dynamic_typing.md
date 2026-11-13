# Topic 2.1: Variables and Dynamic Typing

> Learning goal: Understand Python variables, assignment, dynamic typing, `type()`, naming rules, and why types matter in backend development.

## 1. What is a variable?

A variable is a name that refers to an object (a value) in Python.

```python
name = "Riya"
age = 24
salary = 120000
```

- `name` refers to a string object.
- `age` refers to an integer object.
- `salary` refers to an integer object.

A useful mental model is that a variable is a label bound to an object, rather than a permanently typed box.

## 2. Assignment and reassignment

The `=` operator assigns a name to an object.

```python
age = 24
age = 25
```

The second assignment rebinds `age` to the value `25`.

### Assignment between names

```python
a = 10
b = a
a = 20

print(a)
print(b)
```

Output:

```text
20
10
```

When `b = a` runs, `b` is bound to the object/value that `a` refers to at that moment. Reassigning `a` later does not automatically reassign `b`.

## 3. Dynamic typing

Python is dynamically typed. A name can be rebound to objects of different types during program execution.

```python
value = 100
print(value)

value = "Hello"
print(value)

value = True
print(value)
```

Output:

```text
100
Hello
True
```

**Important:** Dynamic typing does not mean Python has no types. Objects still have types. Python determines and checks types at runtime rather than requiring a variable's type to be declared in advance.

## 4. Python vs JavaScript vs Java

### Python

```python
value = 100
value = "Riya"  # Valid
```

### JavaScript

```javascript
let value = 100;
value = "Riya"; // Valid
```

### Java

```java
int value = 100;
value = 200;       // Valid: another int value
value = "Riya";    // Compile-time type error
```

Java is statically typed. The declared type constrains which values can be assigned to a variable.

**Key distinction:** Static typing does not mean a variable's value cannot change. A Java `int` can be reassigned another integer value, but not a `String`.

## 5. Checking types with `type()`

Python provides the built-in `type()` function.

```python
age = 24
print(type(age))

age = "Riya"
print(type(age))
```

Output:

```text
<class 'int'>
<class 'str'>
```

`type()` returns the type object. When printed, Python displays its representation.

Common built-in types include:
- `int`: whole numbers, such as `24`
- `float`: decimal numbers, such as `24.5`
- `str`: text, such as `"Riya"`
- `bool`: Boolean values, `True` and `False`
- `NoneType`: the type of `None`

## 6. Why data types still matter

Dynamic typing does not mean we can ignore types. Types affect which operations are valid and how values behave.

### Example: incompatible operation

```python
age = "24"
print(age + 1)
```

This raises a `TypeError` because Python does not directly add a string and an integer.

If the input is known to represent a number, conversion may be appropriate:

```python
age = "24"
age_number = int(age)
print(age_number + 1)
```

Output:

```text
25
```

Conversion should be deliberate. For example, `int("twenty-four")` raises a `ValueError`.

### Why this matters in backend APIs

Suppose an API expects an integer age but receives text such as `"twenty-four"`. The backend should validate incoming data before using it.

Validation helps:
- reject malformed or unexpected input,
- prevent type-related failures during operations,
- provide clear client-facing error responses,
- keep application logic predictable.

Dynamic typing does not automatically validate API input or provide security. Frameworks such as FastAPI use validation tools, commonly Pydantic models, to check request data.

## 7. Variable naming rules

Python identifiers:
- Can contain letters, digits, and underscores.
- Cannot start with a digit.
- Cannot contain a hyphen.
- Are case-sensitive.
- Cannot be a reserved Python keyword.

Valid examples:

```python
user_name = "Riya"
age2 = 24
total_amount = 500
_private_value = 10
```

Invalid examples:

```python
2age = 24        # Cannot start with a digit
user-name = "R"  # Hyphen is not allowed in an identifier
class = "A"      # 'class' is a reserved keyword
```

Python conventionally uses `snake_case` for variable and function names. Prefer `user_name` over `userName` when following typical Python style.

## 8. Common mistakes and misconceptions

- **Misconception:** Dynamic typing means Python has no types.  
  **Correction:** Python objects have types; type checks happen at runtime.

- **Misconception:** Static typing means a variable's value cannot change.  
  **Correction:** A statically typed variable can be assigned different values of its declared type.

- **Misconception:** `b = a` means `b` follows future assignments to `a`.  
  **Correction:** The assignment binds `b` to the object/value referred to by `a` at that moment. Reassigning `a` does not reassign `b`.

- **Mistake:** Assuming strings and numbers can always be combined.  
  **Correction:** Operations depend on operand types. Convert or validate values intentionally.

- **Mistake:** Using invalid identifiers such as `2age` or `user-name`.  
  **Correction:** Use valid identifiers such as `age2` and `user_name`.

## 9. Practice exercises

Try each exercise before checking a solution.

### Exercise 1: Assignment and rebinding

Predict the output and explain why:

```python
a = 10
b = a
a = 20

print(a)
print(b)
```

### Exercise 2: Dynamic typing

Is this valid Python? What is the type of `value` after each assignment?

```python
value = 50
value = "Python"
value = True
```

### Exercise 3: Use `type()`

Write a program that assigns an integer, a string, and a Boolean to three variables, then prints the type of each using `type()`.

### Exercise 4: Debug a type error

What error occurs, and how could you fix the code if `age` is intended to be a number?

```python
age = "24"
print(age + 1)
```

### Exercise 5: Identify valid names

Which are valid Python identifiers?

```text
user_name
2age
age2
user-name
_private
class
```

Explain why each invalid name is invalid.

### Exercise 6: Backend validation

An API expects `age` to be an integer but receives the string `"twenty-four"`. Explain why the backend should validate the input before using it in calculations.

## 10. Interview Q&A

### Q1. What is a variable in Python?

A variable is a name bound to an object. The name can be reassigned to refer to another object.

### Q2. What is dynamic typing?

Dynamic typing means a name can refer to objects of different types during execution. Python determines and checks object types at runtime.

### Q3. Does dynamic typing mean Python has no data types?

No. Python objects have types. Dynamic typing means you generally do not declare a variable's type in advance.

### Q4. What is the difference between dynamic typing and static typing?

In Python, a name can be rebound to objects of different types. In statically typed Java, a variable's declared type constrains the values that can be assigned to it.

### Q5. Does a Java `int` variable have to keep the same value?

No. It can be reassigned another integer value. It cannot be assigned an incompatible value such as a string.

### Q6. What does `type()` do?

It returns the type object of the supplied object. For example, `type(24)` returns the `int` type.

### Q7. Why do data types matter in backend development?

Types determine which operations are valid and how values behave. Validating incoming data helps prevent type errors and keeps API behavior predictable.

### Q8. What is the difference between `TypeError` and `ValueError`?

A `TypeError` generally means an operation or function received an object of an inappropriate type. A `ValueError` means the type may be appropriate, but the value itself is unsuitable. For example, `int("twenty-four")` raises `ValueError`.

## 11. Completion checklist

- [ ] I can explain what a variable is.
- [ ] I understand assignment and reassignment.
- [ ] I can explain why `b = a` does not make `b` follow future assignments to `a`.
- [ ] I can explain dynamic typing.
- [ ] I know that dynamic typing does not mean Python has no types.
- [ ] I can use `type()` to inspect values.
- [ ] I can compare Python dynamic typing with Java static typing.
- [ ] I know valid and invalid Python variable names.
- [ ] I can explain why types matter in backend APIs.
- [ ] I can identify a basic `TypeError` and explain how validation or conversion may help.

## Key takeaway

**Dynamic typing removes the need to declare a variable's type in advance. It does not remove the importance of types.** Values still have types, operations still have type requirements, and backend APIs still need input validation.

---

## Progress

- Topic: Variables and Dynamic Typing
- Status: Understanding check passed
- Next topic: Python built-in data types
