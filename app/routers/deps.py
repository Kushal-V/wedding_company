from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core import security
from app.core.config import settings
from app.models.token import TokenData
from app.core.database import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")

async def get_current_admin(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        org_name: str = payload.get("org_name")
        if email is None or org_name is None:
            raise credentials_exception
        token_data = TokenData(email=email, organization_name=org_name)
    except JWTError:
        raise credentials_exception
        
    # Verify user exists in Master DB
    master_db = db.get_master_db()
    org = await master_db["organizations"].find_one({"email": email, "organization_name": org_name})
    if org is None:
        raise credentials_exception
    return org
