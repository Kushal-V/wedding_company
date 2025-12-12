from pydantic import BaseModel, EmailStr
from typing import Optional

class OrganizationCreate(BaseModel):
    organization_name: str
    email: EmailStr
    password: str

class OrganizationUpdate(BaseModel):
    organization_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class OrganizationResponse(BaseModel):
    organization_name: str
    email: EmailStr
    
class AdminLogin(BaseModel):
    email: EmailStr
    password: str
