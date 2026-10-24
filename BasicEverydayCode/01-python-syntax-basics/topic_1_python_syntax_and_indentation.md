# Topic 1: Python Syntax and Indentation

> Learning goal: Understand Python's basic syntax, colons, indentation, code blocks, and how to predict output and debug indentation errors.

## 1. What is syntax?

Syntax is the set of rules for writing code that a programming language can understand.

JavaScript example:

```javascript
if (age >= 18) {
    console.log("Adult");
}
```

Python example:

```python
if age >= 18:
    print("Adult")
```

Key differences:
- Python uses a colon (`:`) after statements such as `if`, `else`, loops, and function definitions.
- Python uses indentation to define code blocks.
- Java and JavaScript conventionally use curly braces (`{}`) to delimit many code blocks.

## 2. Colons and code blocks

A colon indicates that a block follows.

```python
age = 24

if age >= 18:
    print("You are an adult")
    print("You can vote")

print("Program finished")
```

The two indented `print()` statements belong to the `if` block. The final `print()` is outside the block, so it runs regardless of whether the condition is true or false.

## 3. Indentation

Indentation means spaces at the beginning of a line. In Python, indentation is part of the syntax, not just visual formatting.

Use **four spaces per indentation level** as the standard convention. VS Code can usually insert indentation automatically after a line ending in a colon.

### Correct

```python
age = 24

if age >= 18:
    print("Adult")
    print("Eligible by age")

print("Program completed")
```

### Incorrect

```python
age = 24

if age >= 18:
print("Adult")
```

The body of the `if` statement is not indented, so Python raises an `IndentationError`.

## 4. `if` and `else` must align

The `if` and its matching `else` should start at the same indentation level. Their bodies are indented underneath them.

```python
age = 16

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

Output:

```text
Minor
```

Incorrect indentation:

```python
age = 16

if age >= 18:
    print("Adult")
    else:
        print("Minor")
```

Here, `else` is incorrectly indented inside the `if` body. Python raises an `IndentationError`.

## 5. Nested blocks

A block can be nested inside another block. Each level is indented further.

```python
age = 24
has_id = True

if age >= 18:
    if has_id:
        print("Entry allowed")
    else:
        print("ID required")
else:
    print("Entry not allowed")
```

Notice:
- The first `if` checks the age.
- The nested `if` checks `has_id`.
- The first `else` aligns with the nested `if`.
- The final `else` aligns with the outer `if`.

Indentation shows which `if` each `else` belongs to.

## 6. Output prediction

When predicting output:
1. Read the condition.
2. Decide whether it evaluates to `True` or `False`.
3. Follow only the selected branch.
4. Continue executing statements outside the conditional in order.

Example:

```python
age = 16

if age >= 18:
    print("Adult")
else:
    print("Minor")

print("Program completed")
```

Output:

```text
Minor
Program completed
```

`Program completed` is outside the conditional, so it runs after either branch.

## 7. Common mistakes

- Forgetting the colon after `if` or `else`.
- Forgetting to indent the body of a block.
- Indenting `else` further than its matching `if`.
- Using inconsistent indentation levels.
- Accidentally placing a statement inside a block when it should run afterward.
- Assuming indentation is only for readability. In Python, it changes the structure of the program.

## 8. Practice exercises

Try these again without looking at the answers.

### Exercise 1: Write a conditional

Write a program that:
1. Assigns `22` to `age`.
2. Prints `Adult` if `age >= 18`, otherwise prints `Minor`.
3. Prints `Program completed` after the conditional.

Expected output:

```text
Adult
Program completed
```

### Exercise 2: Predict the output

What does this print?

```python
age = 16

if age >= 18:
    print("Adult")
else:
    print("Minor")

print("Done")
```

### Exercise 3: Debug indentation

Correct the indentation:

```python
age = 16

if age >= 18:
    print("Adult")
    else:
        print("Minor")
```

### Exercise 4: Understand block ownership

What changes if `print("Done")` is indented inside the `if` body?

```python
age = 16

if age >= 18:
    print("Adult")
    print("Done")
else:
    print("Minor")
```

Explain whether `Done` prints when `age = 16`, and why.

## 9. Interview Q&A

### Q1. What is indentation in Python?

Indentation is whitespace at the beginning of a line. Python uses it to identify code blocks.

### Q2. Why is indentation important?

It determines which statements belong to blocks such as conditionals, loops, and functions. Incorrect indentation can cause an `IndentationError` or change program behavior.

### Q3. How many spaces should you use?

The standard convention is four spaces per indentation level.

### Q4. How do Python blocks differ from Java and JavaScript blocks?

Python uses indentation to define blocks. Java and JavaScript conventionally use curly braces (`{}`) to delimit blocks.

### Q5. Must `else` align with `if`?

Yes. A matching `else` aligns with its `if`; the statements inside each branch are indented underneath the branch.

### Q6. What is the difference between a syntax/indentation error and a logic error?

A syntax or indentation error prevents Python from correctly parsing the code. A logic error occurs when code runs but does not produce the intended result.

### Q7. What is the output if a statement is outside an `if` block?

It runs after the conditional regardless of which branch was selected, as long as execution reaches that statement.

## 10. Completion checklist

- [ ] I can explain what syntax means.
- [ ] I know why Python uses colons.
- [ ] I can identify which statements belong to a block.
- [ ] I can correctly indent `if` and `else`.
- [ ] I can read nested conditional blocks.
- [ ] I can predict output for true and false conditions.
- [ ] I can fix a basic `IndentationError`.
- [ ] I can explain the difference between Python indentation and braces in Java/JavaScript.
- [ ] I can complete all four exercises without looking at the examples.

## Key takeaway

**In Python, indentation defines the structure of the code.** Keep matching `if` and `else` statements aligned, indent their bodies consistently, and check whether each statement belongs inside or outside a block.

---

## Progress

- Topic: Python syntax and indentation
- Status: Initial exercise and follow-up review passed
- Next topic: Variables and dynamic typing
