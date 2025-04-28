from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    phone: str
    email: EmailStr
    
class UserIn(BaseModel):

    first_name: str
    last_name: str
    username: str
    phone: str
    email: EmailStr
    password: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    phone: str  # Regex for validating international phone numbers
    email: EmailStr  # Validates email format
    password: str  # Ensures password is at least 8 characters
    role: str  # Can be 'Candidate' or 'HR'

class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    username: str
    phone: str  # Consider adding regex validation for phone numbers if necessary
    email: EmailStr  # Validates email format
    role: str

