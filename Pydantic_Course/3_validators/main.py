"""
Module 3: Custom Validators
Practical examples of @field_validator and @model_validator.
"""

from pydantic import BaseModel, field_validator, model_validator
from typing import Optional


# ============================================================================
# EXAMPLE 1: Simple Field Validator
# ============================================================================

class Patient(BaseModel):
    """Patient with field validation."""
    name: str
    age: int
    
    @field_validator('name')
    def validate_name(cls, v):
        """Name must not be empty and at least 3 chars."""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        if len(v) < 3:
            raise ValueError('Name must be at least 3 characters')
        return v.strip().title()  # Convert to title case
    
    @field_validator('age')
    def validate_age(cls, v):
        """Age must be between 0 and 150."""
        if v < 0 or v > 150:
            raise ValueError('Age must be between 0 and 150')
        return v


# Test Example 1
print("=" * 60)
print("EXAMPLE 1: Simple Field Validator")
print("=" * 60)

# Valid patient
patient = Patient(name="john smith", age=30)
print(f"✅ Valid patient: {patient.name}, Age: {patient.age}")

# Name too short
try:
    patient = Patient(name="ab", age=25)
except Exception as e:
    print(f"❌ Error: Name must be at least 3 characters")

# Invalid age (too high)
try:
    patient = Patient(name="Jane", age=200)
except Exception as e:
    print(f"❌ Error: Age must be between 0 and 150")


# ============================================================================
# EXAMPLE 2: Validator for Multiple Fields
# ============================================================================

class User(BaseModel):
    """User with multiple field validation."""
    first_name: str
    last_name: str
    
    @field_validator('first_name', 'last_name')
    def validate_names(cls, v):
        """Both names must be non-empty."""
        if not v or not v.strip():
            raise ValueError('Names cannot be empty')
        return v.strip().title()


# Test Example 2
print("\n" + "=" * 60)
print("EXAMPLE 2: Validator for Multiple Fields")
print("=" * 60)

# Valid user
user = User(first_name="john", last_name="doe")
print(f"✅ Valid user: {user.first_name} {user.last_name}")

# Invalid last name
try:
    user = User(first_name="Jane", last_name="")
except Exception as e:
    print(f"❌ Error: Last name cannot be empty")


# ============================================================================
# EXAMPLE 3: Email Validation
# ============================================================================

class Email(BaseModel):
    """Email with domain validation."""
    email: str
    
    @field_validator('email')
    def validate_email(cls, v):
        """Email must have @ and allowed domain."""
        if '@' not in v:
            raise ValueError('Invalid email format')
        
        local, domain = v.split('@', 1)
        
        if not local or not domain:
            raise ValueError('Invalid email format')
        
        allowed_domains = ['gmail.com', 'company.com', 'example.com']
        if domain not in allowed_domains:
            raise ValueError(f'Email domain "{domain}" not allowed. Use: {", ".join(allowed_domains)}')
        
        return v.lower()


# Test Example 3
print("\n" + "=" * 60)
print("EXAMPLE 3: Email Domain Validation")
print("=" * 60)

# Valid email
email = Email(email="john@GMAIL.COM")
print(f"✅ Valid email: {email.email}")

# Disallowed domain
try:
    email = Email(email="jane@yahoo.com")
except Exception as e:
    print(f"❌ Error: yahoo.com domain not allowed")


# ============================================================================
# EXAMPLE 4: Phone Number Formatting
# ============================================================================

class Contact(BaseModel):
    """Contact with phone formatting."""
    name: str
    phone: str
    
    @field_validator('phone')
    def format_phone(cls, v):
        """Format phone to (XXX) XXX-XXXX."""
        # Remove non-digits
        digits = ''.join(c for c in v if c.isdigit())
        
        if len(digits) != 10:
            raise ValueError('Phone must have 10 digits')
        
        # Format to (XXX) XXX-XXXX
        return f'({digits[:3]}) {digits[3:6]}-{digits[6:]}'


# Test Example 4
print("\n" + "=" * 60)
print("EXAMPLE 4: Phone Number Formatting")
print("=" * 60)

# Valid phone
contact = Contact(name="Alice", phone="5551234567")
print(f"✅ Formatted phone: {contact.phone}")

# Invalid phone
try:
    contact = Contact(name="Bob", phone="555-1234")  # Only 7 digits
except Exception as e:
    print(f"❌ Error: Phone must have 10 digits")


# ============================================================================
# EXAMPLE 5: Before/After Validation Mode
# ============================================================================

class Score(BaseModel):
    """Score with before/after validation."""
    name: str
    points: int
    
    @field_validator('points', mode='before')
    def validate_points_before(cls, v):
        """Validate BEFORE type conversion."""
        # v might be string or int at this point
        if isinstance(v, str):
            if not v.isdigit():
                raise ValueError('Points must be numeric')
            return int(v)
        return v
    
    @field_validator('points', mode='after')
    def validate_points_after(cls, v):
        """Validate AFTER type conversion."""
        # v is guaranteed to be int here
        if v < 0 or v > 100:
            raise ValueError('Points must be between 0 and 100')
        return v


# Test Example 5
print("\n" + "=" * 60)
print("EXAMPLE 5: Before/After Validation Modes")
print("=" * 60)

# Valid score with string input (before mode handles conversion)
score = Score(name="Exam 1", points="85")
print(f"✅ Score: {score.name} = {score.points} points")

# Invalid points (out of range)
try:
    score = Score(name="Exam 2", points=150)
except Exception as e:
    print(f"❌ Error: Points must be between 0 and 100")

# Non-numeric string
try:
    score = Score(name="Exam 3", points="abc")
except Exception as e:
    print(f"❌ Error: Points must be numeric")


# ============================================================================
# EXAMPLE 6: Model Validator (Multiple Fields)
# ============================================================================

class DateRange(BaseModel):
    """Date range with model validation."""
    start_date: str  # Format: YYYY-MM-DD
    end_date: str    # Format: YYYY-MM-DD
    
    @model_validator(mode='after')
    def validate_date_range(self):
        """Start date must be before end date."""
        if self.start_date >= self.end_date:
            raise ValueError('Start date must be before end date')
        return self


# Test Example 6
print("\n" + "=" * 60)
print("EXAMPLE 6: Model Validator (Multiple Fields)")
print("=" * 60)

# Valid date range
date_range = DateRange(start_date="2024-01-01", end_date="2024-12-31")
print(f"✅ Valid range: {date_range.start_date} to {date_range.end_date}")

# Invalid date range
try:
    date_range = DateRange(start_date="2024-12-31", end_date="2024-01-01")
except Exception as e:
    print(f"❌ Error: Start date must be before end date")


# ============================================================================
# EXAMPLE 7: Conditional Validation
# ============================================================================

class Medication(BaseModel):
    """Medication with conditional validation."""
    name: str
    dose: Optional[str] = None
    requires_prescription: bool = False
    
    @model_validator(mode='after')
    def validate_prescription_requirement(self):
        """Prescription meds must have a dose."""
        if self.requires_prescription and not self.dose:
            raise ValueError('Prescription medications must specify a dose')
        return self


# Test Example 7
print("\n" + "=" * 60)
print("EXAMPLE 7: Conditional Validation")
print("=" * 60)

# OTC medication (no prescription required)
med1 = Medication(name="Aspirin", requires_prescription=False)
print(f"✅ OTC: {med1.name} (no dose required)")

# Prescription medication with dose
med2 = Medication(name="Antibiotics", dose="250mg", requires_prescription=True)
print(f"✅ Rx: {med2.name} - {med2.dose}")

# Prescription without dose (error)
try:
    med3 = Medication(name="Oxycodone", requires_prescription=True)
except Exception as e:
    print(f"❌ Error: Prescription medications must specify a dose")


# ============================================================================
# EXAMPLE 8: Value Transformation
# ============================================================================

class Company(BaseModel):
    """Company with field transformation."""
    name: str
    website: str
    
    @field_validator('name')
    def transform_name(cls, v):
        """Transform company name to uppercase."""
        return v.strip().upper()
    
    @field_validator('website')
    def format_website(cls, v):
        """Ensure website starts with https://."""
        v = v.strip().lower()
        if not v.startswith('http'):
            v = f'https://{v}'
        return v


# Test Example 8
print("\n" + "=" * 60)
print("EXAMPLE 8: Value Transformation")
print("=" * 60)

# Valid company
company = Company(name=" google ", website="google.com")
print(f"✅ Transformed:")
print(f"   Name: {company.name}")
print(f"   Website: {company.website}")


# ============================================================================
# EXAMPLE 9: Multiple Validators on One Field
# ============================================================================

class Password(BaseModel):
    """Password with multiple validators."""
    value: str
    
    @field_validator('value')
    def min_length(cls, v):
        """At least 8 characters."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
    
    @field_validator('value')
    def has_digit(cls, v):
        """Must contain at least one digit."""
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @field_validator('value')
    def has_upper(cls, v):
        """Must contain at least one uppercase."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v


# Test Example 9
print("\n" + "=" * 60)
print("EXAMPLE 9: Multiple Validators on One Field")
print("=" * 60)

# Valid password
pwd = Password(value="SecurePass123")
print(f"✅ Valid password")

# Too short
try:
    pwd = Password(value="Pass1")
except Exception as e:
    print(f"❌ Error: Password must be at least 8 characters")

# No uppercase
try:
    pwd = Password(value="securepass123")
except Exception as e:
    print(f"❌ Error: Password must contain at least one uppercase letter")


# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
✅ Field Validator:
   - Validates a single field
   - Can handle one or multiple fields
   - mode='after' (default) or mode='before'

✅ Model Validator:
   - Validates entire model
   - Compare fields with each other
   - Complex cross-field logic

✅ Common uses:
   - Email/phone format validation
   - Data transformation (uppercase, lowercase)
   - Range validation (min/max)
   - Conditional validation (if X then Y)

Next: Learn advanced features in Module 4!
""")
