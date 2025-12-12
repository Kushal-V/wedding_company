from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from app.models.token import TokenData
from app.models.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.services.org_service import OrganizationService

router = APIRouter()

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
        token_data = TokenData(email=email, org_name=org_name)
    except JWTError:
        raise credentials_exception
    return token_data

@router.post("/create", response_model=OrganizationResponse)
async def create_organization(org: OrganizationCreate):
    return await OrganizationService.create_organization(org)

@router.get("/get", response_model=OrganizationResponse)
async def get_organization(
    organization_name: str, 
    current_admin: TokenData = Depends(get_current_admin)
):
    # Requirement: "If the organization does not exist, return an appropriate error."
    # Also implicit requirement: Users should probably only see their OWN organization?
    # "Allow deletion for respective authenticated user only" implies restriction.
    # While `/get` inputs `organization_name`, let's enforce permissions or at least allow it if they are that admin.
    
    if organization_name != current_admin.org_name:
         raise HTTPException(status_code=403, detail="Not authorized to view this organization")

    from app.core.database import db
    master_db = db.get_master_db()
    org = await master_db["organizations"].find_one({"organization_name": organization_name})
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
        
    org["_id"] = str(org["_id"])
    return org

@router.put("/update", response_model=OrganizationResponse)
async def update_organization(
    org: OrganizationUpdate,
    current_admin: TokenData = Depends(get_current_admin)
):
    # Requirement: "Validate that the organization name does not already exist" (Handled in Service)
    # Security: Ensure they are updating THEIR OWN org.
    # But wait, if they change the name, they are essentially changing their identity.
    # The `Input` params are `organization_name`, `email`, `password`.
    # Does `organization_name` in input mean the NEW name or the TARGET?
    # Usually strictly typed REST Puts might use the ID in URL. Here `/org/update` has no ID in URL.
    # So `organization_name` in body is likely the NEW value (or the identifier if not changing).
    
    # We must assume the operation is on the `current_admin.org_name`
    # And the `org.organization_name` is what they want to set it to.
    
    return await OrganizationService.update_organization(current_admin.org_name, org)

@router.delete("/delete")
async def delete_organization(
    organization_name: str,
    current_admin: TokenData = Depends(get_current_admin)
):
    # Requirement: "Allow deletion for respective authenticated user only"
    if organization_name != current_admin.org_name:
        raise HTTPException(status_code=403, detail="Not authorized to delete this organization")
    
    await OrganizationService.delete_organization(organization_name)
    return {"message": "Organization deleted successfully"}
