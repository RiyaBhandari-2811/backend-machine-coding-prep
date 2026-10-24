# Topic 2: Variables, Naming, and Dynamic Typing

> Learning goal: Understand what variables are, how to name them well, and how Python's dynamic typing differs from statically typed languages like Java.

## 1. What is a variable?

A variable is a named reference to a value stored in memory.

Python example:

```python
age = 22
name = "Alice"
```

JavaScript example:

```javascript
let age = 22;
let name = "Alice";
```

Java example:

```java
int age = 22;
String name = "Alice";
```

## 2. Naming conventions

- Use descriptive names: `userAge` instead of `a`.
- Python uses `snake_case` for variables and functions (`user_age`).
- JavaScript and Java use `camelCase` for variables (`userAge`).
- Constants are usually written in `UPPER_SNAKE_CASE` (`MAX_SIZE`).
- Names must start with a letter or underscore, not a digit.
- Avoid reserved keywords (`if`, `class`, `for`, etc.).

## 3. Dynamic typing

In Python, you do not declare a type. The type is bound to the value, and a variable can be reassigned to a value of a different type.

```python
x = 10        # int
x = "hello"   # now a str
x = 3.14      # now a float
```

Use `type()` to inspect the current type:

```python
x = 10
print(type(x))   # <class 'int'>
x = "hello"
print(type(x))   # <class 'str'>
```

## 4. Static typing (for contrast)

Java is statically typed. The type is fixed at declaration, and assigning a value of a different type causes a compile error.

```java
int x = 10;
x = "hello"; // compile error: incompatible types
```

## 5. Common mistakes

- Using a variable before assigning it (`NameError` in Python).
- Confusing assignment (`=`) with equality comparison (`==`).
- Overwriting a variable unintentionally by reusing its name.
- Relying on a variable's type after it may have been reassigned.
