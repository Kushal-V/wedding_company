from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class OrganizationBase(BaseModel):
    organization_name: str
    email: EmailStr

class OrganizationCreate(OrganizationBase):
    password: str

class OrganizationUpdate(OrganizationBase):
    password: str

class OrganizationResponse(OrganizationBase):
    id: str = Field(alias="_id")
    collection_name: str
    
    class Config:
        populate_by_name = True

class AdminLogin(BaseModel):
    email: EmailStr
    password: str
