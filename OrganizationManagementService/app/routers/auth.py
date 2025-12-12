from fastapi import APIRouter, HTTPException, status
from app.models.organization import AdminLogin
from app.models.token import Token
from app.core.database import db
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: AdminLogin):
    master_db = db.get_master_db()
    org_coll = master_db["organizations"]
    
    # 1. Validate email
    user = await org_coll.find_one({"email": form_data.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Validate password
    if not verify_password(form_data.password, user["password"]):
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generate Token
    # Requirement: Return Admin identification, Organization identifier
    access_token = create_access_token(
        subject=user["email"], 
        org_name=user["organization_name"]
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "organization_name": user["organization_name"]
    }
