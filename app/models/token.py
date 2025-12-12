from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    organization_name: str

class TokenData(BaseModel):
    email: Optional[str] = None
    organization_name: Optional[str] = None
