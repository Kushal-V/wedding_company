from fastapi import APIRouter, Depends, HTTPException
from app.models.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.services.org_service import OrganizationService
from app.routers.deps import get_current_admin

router = APIRouter()

@router.post("/create", response_model=dict)
async def create_organization(org: OrganizationCreate):
    return await OrganizationService.create_organization(org)

@router.get("/get", response_model=OrganizationResponse)
async def get_organization(current_user: dict = Depends(get_current_admin)):
    # current_user is the org document from master_db
    return current_user

@router.put("/update")
async def update_organization(
    org_update: OrganizationUpdate, 
    current_user: dict = Depends(get_current_admin)
):
    return await OrganizationService.update_organization(current_user["organization_name"], org_update)

@router.delete("/delete")
async def delete_organization(current_user: dict = Depends(get_current_admin)):
    return await OrganizationService.delete_organization(current_user["organization_name"])
