"""
Module 4: Advanced Pydantic Features
Practical examples of nested models, computed fields, and model export.
"""

from pydantic import BaseModel, Field, computed_field
from typing import Optional, List
from datetime import datetime


# ============================================================================
# EXAMPLE 1: Nested Models (Composition)
# ============================================================================

class Address(BaseModel):
    """Address model - can be reused in multiple places."""
    street: str = Field(..., min_length=5)
    city: str = Field(..., min_length=2)
    country: str = Field(..., min_length=2)
    zipcode: str = Field(..., pattern="^[0-9]{5}(-[0-9]{4})?$")


class Patient(BaseModel):
    """Patient with nested Address."""
    name: str = Field(..., min_length=1)
    age: int = Field(..., gt=0, le=150)
    email: str
    address: Address  # Nested model


# Test Example 1
print("=" * 60)
print("EXAMPLE 1: Nested Models (Composition)")
print("=" * 60)

# Valid nested data
patient_data = {
    "name": "John Smith",
    "age": 30,
    "email": "john@example.com",
    "address": {
        "street": "123 Main Street",
        "city": "Boston",
        "country": "USA",
        "zipcode": "02101"
    }
}

patient = Patient(**patient_data)
print(f"✅ Patient: {patient.name}")
print(f"   Lives in: {patient.address.street}, {patient.address.city}")

# Accessing nested fields
print(f"   Zipcode: {patient.address.zipcode}")

# Invalid nested data (bad zipcode)
try:
    bad_data = {
        "name": "Jane",
        "age": 25,
        "email": "jane@example.com",
        "address": {
            "street": "456 Oak Ave",
            "city": "NYC",
            "country": "USA",
            "zipcode": "123"  # Invalid format
        }
    }
    patient = Patient(**bad_data)
except Exception as e:
    print(f"❌ Error: Invalid zipcode format")


# ============================================================================
# EXAMPLE 2: Computed Fields
# ============================================================================

class Rectangle(BaseModel):
    """Rectangle with computed area and perimeter."""
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    
    @computed_field
    @property
    def area(self) -> float:
        """Computed: width * height."""
        return self.width * self.height
    
    @computed_field
    @property
    def perimeter(self) -> float:
        """Computed: 2 * (width + height)."""
        return 2 * (self.width + self.height)
    
    @computed_field
    @property
    def is_square(self) -> bool:
        """Computed: check if width equals height."""
        return abs(self.width - self.height) < 0.001


# Test Example 2
print("\n" + "=" * 60)
print("EXAMPLE 2: Computed Fields")
print("=" * 60)

rect = Rectangle(width=5, height=3)
print(f"✅ Rectangle: {rect.width} x {rect.height}")
print(f"   Area: {rect.area}")
print(f"   Perimeter: {rect.perimeter}")
print(f"   Is Square: {rect.is_square}")

# Computed fields in model_dump
print(f"\n   As dict: {rect.model_dump()}")


# ============================================================================
# EXAMPLE 3: Computed Medical Metrics
# ============================================================================

class MedicalPatient(BaseModel):
    """Patient with computed medical metrics."""
    name: str
    weight_kg: float = Field(..., gt=0)
    height_m: float = Field(..., gt=0)
    age: int = Field(..., gt=0)
    
    @computed_field
    @property
    def bmi(self) -> float:
        """BMI = weight / (height ^ 2)."""
        return round(self.weight_kg / (self.height_m ** 2), 2)
    
    @computed_field
    @property
    def bmi_category(self) -> str:
        """BMI category."""
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    @computed_field
    @property
    def age_group(self) -> str:
        """Age group."""
        if self.age < 18:
            return "Minor"
        elif self.age < 65:
            return "Adult"
        else:
            return "Senior"


# Test Example 3
print("\n" + "=" * 60)
print("EXAMPLE 3: Computed Medical Metrics")
print("=" * 60)

patient = MedicalPatient(name="Alice", weight_kg=65, height_m=1.70, age=30)
print(f"✅ Patient: {patient.name}")
print(f"   Height: {patient.height_m}m, Weight: {patient.weight_kg}kg")
print(f"   BMI: {patient.bmi} ({patient.bmi_category})")
print(f"   Age Group: {patient.age_group}")


# ============================================================================
# EXAMPLE 4: Export to Dictionary
# ============================================================================

class Employee(BaseModel):
    """Employee for export examples."""
    employee_id: int
    name: str
    email: str
    department: str
    salary: float


# Test Example 4
print("\n" + "=" * 60)
print("EXAMPLE 4: Export to Dictionary")
print("=" * 60)

emp = Employee(
    employee_id=101,
    name="Bob Johnson",
    email="bob@company.com",
    department="Engineering",
    salary=75000
)

# Full export
full_dict = emp.model_dump()
print(f"✅ Full export: {full_dict}")

# Include only specific fields
public_info = emp.model_dump(include={'name', 'department'})
print(f"✅ Public info: {public_info}")

# Exclude specific fields
private_info = emp.model_dump(exclude={'salary'})
print(f"✅ Exclude salary: {private_info}")


# ============================================================================
# EXAMPLE 5: Export to JSON String
# ============================================================================

class Book(BaseModel):
    """Book for JSON export."""
    title: str
    author: str
    pages: int
    published: datetime


# Test Example 5
print("\n" + "=" * 60)
print("EXAMPLE 5: Export to JSON String")
print("=" * 60)

book = Book(
    title="Python Basics",
    author="John Doe",
    pages=350,
    published=datetime(2023, 1, 15)
)

# JSON export (compact)
json_compact = book.model_dump_json()
print(f"✅ Compact JSON: {json_compact}")

# JSON export (pretty)
json_pretty = book.model_dump_json(indent=2)
print(f"\n✅ Pretty JSON:\n{json_pretty}")


# ============================================================================
# EXAMPLE 6: Complex Nesting with Lists
# ============================================================================

class Contact(BaseModel):
    """Contact information."""
    email: str
    phone: Optional[str] = None


class HospitalPatient(BaseModel):
    """Hospital patient with complex nesting."""
    name: str
    age: int
    address: Address  # Single nested
    contacts: List[Contact]  # List of nested models
    medications: List[str] = Field(default=[])


# Test Example 6
print("\n" + "=" * 60)
print("EXAMPLE 6: Complex Nesting with Lists")
print("=" * 60)

hospital_patient_data = {
    "name": "Carol",
    "age": 45,
    "address": {
        "street": "789 Maple Drive",
        "city": "Portland",
        "country": "USA",
        "zipcode": "97201"
    },
    "contacts": [
        {"email": "carol@example.com", "phone": "555-1234"},
        {"email": "carol.work@company.com"}
    ],
    "medications": ["Aspirin", "Metformin"]
}

hospital_patient = HospitalPatient(**hospital_patient_data)
print(f"✅ Hospital Patient: {hospital_patient.name}")
print(f"   Address: {hospital_patient.address.city}, {hospital_patient.address.country}")
print(f"   Contacts: {len(hospital_patient.contacts)}")
print(f"   Medications: {', '.join(hospital_patient.medications)}")


# ============================================================================
# EXAMPLE 7: Partial Export with Exclude
# ============================================================================

class SensitiveData(BaseModel):
    """Data with sensitive fields."""
    user_id: int
    username: str
    email: str
    password_hash: str
    api_key: str


# Test Example 7
print("\n" + "=" * 60)
print("EXAMPLE 7: Partial Export with Exclude")
print("=" * 60)

user = SensitiveData(
    user_id=1001,
    username="johndoe",
    email="john@example.com",
    password_hash="$2b$12$...",
    api_key="sk_live_abc123xyz"
)

# Export without sensitive data
safe_export = user.model_dump(exclude={'password_hash', 'api_key'})
print(f"✅ Safe export (sensitive excluded):")
print(f"   {safe_export}")

# Export only safe fields
safe_include = user.model_dump(include={'user_id', 'username', 'email'})
print(f"✅ Safe export (only public fields):")
print(f"   {safe_include}")


# ============================================================================
# EXAMPLE 8: API Response Pattern
# ============================================================================

class PatientResponse(BaseModel):
    """Response model for API."""
    id: int
    name: str
    email: str
    age: int
    
    @computed_field
    @property
    def is_adult(self) -> bool:
        return self.age >= 18
    
    def to_dict(self):
        """Convert to dict for API response."""
        return self.model_dump()
    
    def to_json(self):
        """Convert to JSON for API response."""
        return self.model_dump_json()


# Test Example 8
print("\n" + "=" * 60)
print("EXAMPLE 8: API Response Pattern")
print("=" * 60)

response = PatientResponse(id=1, name="David", email="david@example.com", age=28)
print(f"✅ API Response object")
print(f"   Name: {response.name}")
print(f"   Is Adult: {response.is_adult}")

# Convert for API
print(f"\n   As dict: {response.to_dict()}")
print(f"   As JSON: {response.to_json()}")


# ============================================================================
# EXAMPLE 9: Nested with Computed Fields
# ============================================================================

class Order(BaseModel):
    """Order with computed total."""
    order_id: int
    customer_name: str
    items: List[dict]  # [{name, price, quantity}, ...]
    tax_rate: float = 0.1
    
    @computed_field
    @property
    def subtotal(self) -> float:
        """Sum of all items."""
        return sum(item.get('price', 0) * item.get('quantity', 0) 
                  for item in self.items)
    
    @computed_field
    @property
    def tax_amount(self) -> float:
        """Tax calculation."""
        return round(self.subtotal * self.tax_rate, 2)
    
    @computed_field
    @property
    def total(self) -> float:
        """Total with tax."""
        return round(self.subtotal + self.tax_amount, 2)


# Test Example 9
print("\n" + "=" * 60)
print("EXAMPLE 9: Nested with Computed Fields")
print("=" * 60)

order = Order(
    order_id=5001,
    customer_name="Eve",
    items=[
        {"name": "Laptop", "price": 999, "quantity": 1},
        {"name": "Mouse", "price": 29, "quantity": 2}
    ],
    tax_rate=0.08
)
print(f"✅ Order #{order.order_id} for {order.customer_name}")
print(f"   Subtotal: ${order.subtotal}")
print(f"   Tax (8%): ${order.tax_amount}")
print(f"   Total: ${order.total}")

# Export shows computed fields
print(f"\n   Full export: {order.model_dump()}")


# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
✅ Nested Models:
   - Organize complex data structures
   - Reusable models (Address, Contact, etc.)
   - Each nested model is validated

✅ Computed Fields (@computed_field):
   - Fields calculated from other fields
   - Included in model_dump() output
   - Great for derived values (area, BMI, total)

✅ Model Export:
   - model_dump() → dict
   - model_dump_json() → JSON string
   - include/exclude for partial export
   - exclude_unset for delta exports

✅ Use Cases:
   - API responses and requests
   - Database models
   - Configuration management
   - ML model validation

🎉 Congratulations! You've mastered Pydantic!
""")
