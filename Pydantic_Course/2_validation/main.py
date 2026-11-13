"""
Module 2: Data Validation with Field
Practical examples of using Field() for validation constraints.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============================================================================
# EXAMPLE 1: Required Fields with Constraints
# ============================================================================

class Patient(BaseModel):
    """Patient with Field validation constraints."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Patient full name"
    )
    age: int = Field(
        ...,
        gt=0,
        le=150,
        description="Patient age (0-150)"
    )
    patient_id: str = Field(
        ...,
        pattern="^P[0-9]{3}$",
        description="Patient ID format: P001, P002, etc."
    )


# Test Example 1
print("=" * 60)
print("EXAMPLE 1: Required Fields with Constraints")
print("=" * 60)

# Valid data
try:
    patient = Patient(name="John Smith", age=30, patient_id="P001")
    print(f"✅ Valid patient: {patient.name}, Age: {patient.age}")
except Exception as e:
    print(f"❌ Error: {e}")

# Invalid age (negative)
try:
    patient = Patient(name="Jane", age=-5, patient_id="P002")
    print(f"✅ Patient: {patient.name}")
except Exception as e:
    print(f"❌ Error: Age can't be negative")

# Invalid name (empty)
try:
    patient = Patient(name="", age=25, patient_id="P003")
except Exception as e:
    print(f"❌ Error: Name can't be empty (min_length=1)")

# Invalid patient_id format
try:
    patient = Patient(name="Bob", age=40, patient_id="INVALID")
except Exception as e:
    print(f"❌ Error: patient_id must match pattern P[0-9]{{3}}")


# ============================================================================
# EXAMPLE 2: Optional Fields with Defaults
# ============================================================================

class Employee(BaseModel):
    """Employee with optional fields."""
    name: str = Field(..., min_length=1)
    employee_id: int = Field(..., gt=0)
    phone: Optional[str] = Field(None, min_length=10)
    department: str = Field(default="General", description="Department name")
    is_active: bool = Field(default=True)


# Test Example 2
print("\n" + "=" * 60)
print("EXAMPLE 2: Optional Fields with Defaults")
print("=" * 60)

# Only required fields
emp1 = Employee(name="Alice", employee_id=101)
print(f"✅ Employee with defaults:")
print(f"   {emp1.name}, Dept: {emp1.department}, Active: {emp1.is_active}")

# All fields
emp2 = Employee(
    name="Bob",
    employee_id=102,
    phone="5551234567",
    department="Engineering",
    is_active=False
)
print(f"✅ Employee with all fields: {emp2.name}, Phone: {emp2.phone}")


# ============================================================================
# EXAMPLE 3: Numeric Constraints
# ============================================================================

class Product(BaseModel):
    """Product with numeric constraints."""
    name: str
    price: float = Field(gt=0, description="Price must be positive")
    quantity: int = Field(ge=0, le=10000, description="Quantity 0-10000")
    rating: float = Field(ge=0, le=5, description="Rating 0-5 stars")


# Test Example 3
print("\n" + "=" * 60)
print("EXAMPLE 3: Numeric Constraints")
print("=" * 60)

# Valid product
product = Product(
    name="Laptop",
    price=999.99,
    quantity=50,
    rating=4.5
)
print(f"✅ Valid product: {product.name}")
print(f"   Price: ${product.price}, Qty: {product.quantity}, Rating: {product.rating}★")

# Invalid price (zero)
try:
    product = Product(name="Mouse", price=0, quantity=100, rating=4.0)
except Exception as e:
    print(f"❌ Error: Price must be > 0")

# Invalid rating (too high)
try:
    product = Product(name="Keyboard", price=79.99, quantity=50, rating=6.0)
except Exception as e:
    print(f"❌ Error: Rating must be ≤ 5")


# ============================================================================
# EXAMPLE 4: String Constraints
# ============================================================================

class User(BaseModel):
    """User with string constraints."""
    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Username 3-20 characters"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password min 8 characters"
    )
    bio: Optional[str] = Field(None, max_length=500)


# Test Example 4
print("\n" + "=" * 60)
print("EXAMPLE 4: String Constraints")
print("=" * 60)

# Valid user
user = User(
    username="johndoe",
    password="SecurePassword123",
    bio="Software developer"
)
print(f"✅ Valid user: {user.username}")

# Too short username
try:
    user = User(username="ab", password="Password123")
except Exception as e:
    print(f"❌ Error: Username too short (min_length=3)")

# Too short password
try:
    user = User(username="valid_user", password="short")
except Exception as e:
    print(f"❌ Error: Password too short (min_length=8)")


# ============================================================================
# EXAMPLE 5: List Constraints
# ============================================================================

class Team(BaseModel):
    """Team with list constraints."""
    name: str
    members: List[str] = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Team members 1-10"
    )
    skills: List[str] = Field(
        default=[],
        max_length=20,
        description="Max 20 skills"
    )


# Test Example 5
print("\n" + "=" * 60)
print("EXAMPLE 5: List Constraints")
print("=" * 60)

# Valid team
team = Team(
    name="Python Team",
    members=["Alice", "Bob", "Carol"],
    skills=["Python", "FastAPI", "PostgreSQL"]
)
print(f"✅ Team: {team.name}")
print(f"   Members ({len(team.members)}): {', '.join(team.members)}")

# Empty members list (invalid)
try:
    team = Team(name="Empty Team", members=[])
except Exception as e:
    print(f"❌ Error: Team must have at least 1 member (min_length=1)")

# Too many members
try:
    team = Team(
        name="Big Team",
        members=[f"Member{i}" for i in range(15)]
    )
except Exception as e:
    print(f"❌ Error: Team can't have more than 10 members (max_length=10)")


# ============================================================================
# EXAMPLE 6: Type Coercion
# ============================================================================

class Order(BaseModel):
    """Order demonstrating type coercion."""
    order_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


# Test Example 6
print("\n" + "=" * 60)
print("EXAMPLE 6: Type Coercion")
print("=" * 60)

# Pydantic converts compatible types
order = Order(
    order_id="12345",    # String converted to int
    quantity="10",       # String converted to int
    price="99.99"        # String converted to float
)
print(f"✅ Order created with type coercion:")
print(f"   ID: {order.order_id} (int)")
print(f"   Qty: {order.quantity} (int)")
print(f"   Price: ${order.price} (float)")


# ============================================================================
# EXAMPLE 7: Strict Mode (No Coercion)
# ============================================================================

class StrictOrder(BaseModel):
    """Order with strict mode (no type coercion)."""
    order_id: int = Field(..., strict=True, gt=0)
    quantity: int = Field(..., strict=True, gt=0)


# Test Example 7
print("\n" + "=" * 60)
print("EXAMPLE 7: Strict Mode (No Type Coercion)")
print("=" * 60)

# Strict mode: must have exact type
try:
    order = StrictOrder(order_id=101, quantity=5)
    print(f"✅ Strict order: ID={order.order_id}, Qty={order.quantity}")
except Exception as e:
    print(f"Error: {e}")

# Won't coerce string to int in strict mode
try:
    order = StrictOrder(order_id="101", quantity=5)
except Exception as e:
    print(f"❌ Error: Strict mode rejects type coercion (string→int)")


# ============================================================================
# EXAMPLE 8: Metadata for Documentation
# ============================================================================

class Article(BaseModel):
    """Article with metadata for documentation."""
    title: str = Field(
        ...,
        title="Article Title",
        description="The main heading of the article",
        min_length=5,
        max_length=200
    )
    content: str = Field(
        ...,
        description="Full article content",
        min_length=10
    )
    author: str = Field(
        ...,
        description="Author name",
        examples=["John Smith", "Jane Doe"]
    )
    published: bool = Field(
        default=False,
        description="Has this article been published?"
    )


# Test Example 8
print("\n" + "=" * 60)
print("EXAMPLE 8: Metadata for Documentation")
print("=" * 60)

article = Article(
    title="Introduction to Pydantic",
    content="Pydantic is a Python library for data validation using type annotations...",
    author="Alice Johnson"
)
print(f"✅ Article: {article.title}")
print(f"   By: {article.author}")
print(f"   Published: {article.published}")

# Show model schema (used in API docs)
print("\n📋 Model Schema:")
schema = Article.model_json_schema()
print(f"   Fields: {list(schema['properties'].keys())}")


# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
✅ Field() provides:
   1. Validation constraints (gt, ge, lt, le, min/max_length)
   2. String patterns (regex validation)
   3. Metadata (title, description, examples)
   4. Default values
   5. Type coercion control (strict mode)

✅ Common constraints:
   - gt/ge/lt/le - for numbers
   - min_length/max_length - for strings and lists
   - pattern - for regex matching

Next: Learn custom validators in Module 3!
""")
