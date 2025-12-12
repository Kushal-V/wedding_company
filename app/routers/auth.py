from fastapi import APIRouter, HTTPException, status
from app.models.organization import AdminLogin
from app.models.token import Token
from app.core.database import db
from app.core import security
from datetime import timedelta

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: AdminLogin):
    master_db = db.get_master_db()
    # Find organization by email (assuming email is unique admin for an org)
    # Actually email might not be unique globally, but for this assignment simpler.
    # But wait, login request only has email/password. How do we know which org?
    # Assignment: "Admin Login: Input: email, password".
    # So email must be unique or we pick first? "Validate unique organization name" is required.
    # We should assume email is unique for admin login.
    
    user = await master_db["organizations"].find_one({"email": form_data.email})
    if not user or not security.verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user["email"],
        org_name=user["organization_name"],
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "organization_name": user["organization_name"]
    }
