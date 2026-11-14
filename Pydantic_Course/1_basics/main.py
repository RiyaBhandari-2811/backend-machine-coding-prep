"""
Module 1: Pydantic Basics
Practical examples of creating and using basic Pydantic models.
"""

from pydantic import BaseModel
from typing import Optional, List


# ============================================================================
# EXAMPLE 1: Basic Model
# ============================================================================

class Patient(BaseModel):
    """Simple patient model with required fields."""
    name: str
    age: int
    email: str


# Test Example 1
print("=" * 60)
print("EXAMPLE 1: Basic Model")
print("=" * 60)

# Valid data - works
patient1 = Patient(name="John", age=30, email="john@example.com")
print(f"✅ Valid patient: {patient1}")
print(f"   Name: {patient1.name}")
print(f"   Age: {patient1.age}")

# Invalid data - will raise ValidationError
try:
    patient2 = Patient(name="Alice", age="twenty-five", email="alice@example.com")
except Exception as e:
    print(f"❌ Error: age must be integer, got string")


# ============================================================================
# EXAMPLE 2: Optional Fields
# ============================================================================

class Employee(BaseModel):
    """Employee model with optional fields."""
    name: str
    employee_id: int
    phone: Optional[str] = None  # Optional, defaults to None


# Test Example 2
print("\n" + "=" * 60)
print("EXAMPLE 2: Optional Fields")
print("=" * 60)

# Without optional field
emp1 = Employee(name="Bob", employee_id=101)
print(f"✅ Employee without phone: {emp1}")
print(f"   Phone value: {emp1.phone}")

# With optional field
emp2 = Employee(name="Carol", employee_id=102, phone="555-1234")
print(f"✅ Employee with phone: {emp2}")
print(f"   Phone value: {emp2.phone}")


# ============================================================================
# EXAMPLE 3: Default Values
# ============================================================================

class Product(BaseModel):
    """Product model with default values."""
    name: str
    price: float
    in_stock: bool = True  # Default to True
    quantity: int = 0      # Default to 0


# Test Example 3
print("\n" + "=" * 60)
print("EXAMPLE 3: Default Values")
print("=" * 60)

# Using defaults
product1 = Product(name="Laptop", price=999.99)
print(f"✅ Product with defaults: {product1}")
print(f"   in_stock: {product1.in_stock} (default)")
print(f"   quantity: {product1.quantity} (default)")

# Overriding defaults
product2 = Product(name="Mouse", price=29.99, in_stock=False, quantity=5)
print(f"✅ Product with overrides: {product2}")


# ============================================================================
# EXAMPLE 4: Type Conversion
# ============================================================================

class Order(BaseModel):
    """Order model - Pydantic can convert compatible types."""
    order_id: int
    quantity: int
    price: float


# Test Example 4
print("\n" + "=" * 60)
print("EXAMPLE 4: Type Conversion")
print("=" * 60)

# Pydantic converts compatible types
order = Order(order_id="12345", quantity="10", price="99.99")
print(f"✅ Order created with type conversion:")
print(f"   order_id: {order.order_id} (type: {type(order.order_id).__name__})")
print(f"   quantity: {order.quantity} (type: {type(order.quantity).__name__})")
print(f"   price: {order.price} (type: {type(order.price).__name__})")


# ============================================================================
# EXAMPLE 5: Complex Types
# ============================================================================

class Hospital(BaseModel):
    """Hospital model with complex types."""
    name: str
    departments: List[str]          # List of strings
    contact_info: dict              # Dictionary


# Test Example 5
print("\n" + "=" * 60)
print("EXAMPLE 5: Complex Types")
print("=" * 60)

hospital = Hospital(
    name="City Medical Center",
    departments=["Emergency", "Surgery", "Pediatrics"],
    contact_info={
        "phone": "555-0100",
        "email": "info@cityhospital.com",
        "address": "123 Medical Ave"
    }
)
print(f"✅ Hospital: {hospital.name}")
print(f"   Departments: {hospital.departments}")
print(f"   Contact: {hospital.contact_info}")


# ============================================================================
# EXAMPLE 6: Accessing Model Data
# ============================================================================

class Student(BaseModel):
    """Simple student model."""
    student_id: int
    name: str
    grade: str


# Test Example 6
print("\n" + "=" * 60)
print("EXAMPLE 6: Accessing Model Data")
print("=" * 60)

student = Student(student_id=1001, name="David", grade="A")
print(f"✅ Student instance: {student}")

# Access individual fields
print(f"   ID: {student.student_id}")
print(f"   Name: {student.name}")
print(f"   Grade: {student.grade}")

# Get as dictionary
student_dict = student.model_dump()
print(f"   As dictionary: {student_dict}")

# Get as JSON string
student_json = student.model_dump_json()
print(f"   As JSON: {student_json}")


# ============================================================================
# EXAMPLE 7: Error Handling
# ============================================================================

class Book(BaseModel):
    """Book model for error handling demo."""
    title: str
    author: str
    pages: int
    rating: float


# Test Example 7
print("\n" + "=" * 60)
print("EXAMPLE 7: Error Handling")
print("=" * 60)

# Valid book
book = Book(title="Python Basics", author="John Doe", pages=300, rating=4.5)
print(f"✅ Valid book: {book.title}")

# Missing required field
try:
    invalid_book = Book(title="Some Book", author="Author")  # Missing pages and rating
except Exception as e:
    print(f"❌ Error: Missing required fields")
    print(f"   {str(e)[:100]}...")  # Show first 100 chars of error

# Wrong data type
try:
    invalid_book = Book(title="Book", author="Author", pages="three hundred", rating=4.5)
except Exception as e:
    print(f"❌ Error: Wrong data type for 'pages'")


# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
✅ Pydantic provides:
   1. Type validation - automatic checking of data types
   2. Optional fields - fields that can be None
   3. Default values - pre-set field values
   4. Type conversion - automatic conversion of compatible types
   5. Complex types - support for lists, dicts, etc.
   6. Error messages - clear validation errors

✅ Key methods:
   - model.model_dump() - Convert to dict
   - model.model_dump_json() - Convert to JSON string

Next: Learn about data validation constraints in Module 2!
""")
