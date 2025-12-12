from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    organization_name: str  # Requirement: Organization identifier/ID

class TokenData(BaseModel):
    email: Optional[str] = None
    org_name: Optional[str] = None
