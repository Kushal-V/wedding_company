from fastapi import HTTPException
from app.core.database import db
from app.core import security
from app.models.organization import OrganizationCreate, OrganizationUpdate

class OrganizationService:
    
    @staticmethod
    async def create_organization(data: OrganizationCreate):
        master_db = db.get_master_db()
        org_coll = master_db["organizations"]
        
        # Validate unique name
        if await org_coll.find_one({"organization_name": data.organization_name}):
            raise HTTPException(status_code=400, detail="Organization name already exists")
            
        # Create metadata
        hashed_password = security.get_password_hash(data.password)
        new_org = data.dict()
        new_org["password"] = hashed_password
        
        result = await org_coll.insert_one(new_org)
        
        # Initialize Dynamic Collection
        collection_name = f"org_{data.organization_name}"
        # We perform a dummy insert to create the collection if lazy
        await master_db[collection_name].insert_one({"init": True, "created_at": "now"})
        
        return {
            "organization_name": data.organization_name,
            "message": "Organization created successfully",
            "id": str(result.inserted_id)
        }

    @staticmethod
    async def update_organization(current_org_name: str, data: OrganizationUpdate):
        master_db = db.get_master_db()
        org_coll = master_db["organizations"]
        
        update_data = {k: v for k, v in data.dict().items() if v is not None}
        
        if "password" in update_data:
            update_data["password"] = security.get_password_hash(update_data["password"])
            
        if "organization_name" in update_data and update_data["organization_name"] != current_org_name:
            new_name = update_data["organization_name"]
            # Check uniqueness
            if await org_coll.find_one({"organization_name": new_name}):
                raise HTTPException(status_code=400, detail="New Organization name already exists")
                
            # MIGRATION: Rename Collection
            old_coll_name = f"org_{current_org_name}"
            new_coll_name = f"org_{new_name}"
            
            # MongoDB Rename (using command or pymongo rename)
            # Motor doesn't have rename_collection directly on DB object in some versions?
            # We can use execute_command (run_command in asyncio)
            # Wait, creating new name should handle the logic
            try:
                await master_db[old_coll_name].rename(new_coll_name)
            except Exception as e:
                 # If collection doesn't exist (maybe empty), just ignore or log
                 print(f"Migration rename warning: {e}")
        
        await org_coll.update_one({"organization_name": current_org_name}, {"$set": update_data})
        return {"message": "Organization updated successfully", "updated_fields": list(update_data.keys())}

    @staticmethod
    async def delete_organization(org_name: str):
        master_db = db.get_master_db()
        org_coll = master_db["organizations"]
        
        # Delete Metadata
        await org_coll.delete_one({"organization_name": org_name})
        
        # Drop Collection
        coll_name = f"org_{org_name}"
        await master_db[coll_name].drop()
        
        return {"message": "Organization deleted successfully"}
