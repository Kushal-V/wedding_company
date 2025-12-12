from app.core.database import db
from app.core.security import get_password_hash
from fastapi import HTTPException, status

class OrganizationService:
    
    @staticmethod
    async def create_organization(data):
        print("DEBUG: Starting create_organization")
        master_db = db.get_master_db()
        org_coll = master_db["organizations"]
        
        # 1. Validate org name existence
        print(f"DEBUG: Checking existence of {data.organization_name}")
        existing_org = await org_coll.find_one({"organization_name": data.organization_name})
        if existing_org:
            raise HTTPException(status_code=400, detail="Organization name already exists")
        
        # 2. Setup metadata
        print("DEBUG: Setting up metadata")
        collection_name = f"org_{data.organization_name}"
        hashed_password = get_password_hash(data.password)
        
        new_org = {
            "organization_name": data.organization_name,
            "email": data.email,
            "password": hashed_password,
            "collection_name": collection_name,
            # "connection_details": {} # If we had separate DBs
        }
        
        # 3. Store in Master DB
        print("DEBUG: Inserting into Master DB")
        result = await org_coll.insert_one(new_org)
        print("DEBUG: Inserted")
        
        # 4. Create Dynamic Collection (implicitly created on first insert, but we can explicitly create or insert a dummy doc)
        # Requirement: "The collection can be empty or initialized with a basic schema"
        print("DEBUG: Initializing dynamic collection")
        dynamic_coll = db.get_dynamic_collection(data.organization_name)
        await dynamic_coll.insert_one({"info": "Collection Initialized", "created_at": "now"})
        print("DEBUG: Dynamic collection initialized")
        
        created_org = await org_coll.find_one({"_id": result.inserted_id})
        created_org["_id"] = str(created_org["_id"])
        return created_org

    @staticmethod
    async def update_organization(current_org_name: str, data):
        master_db = db.get_master_db()
        org_coll = master_db["organizations"]
        
        # 1. Check if name is changing
        if data.organization_name != current_org_name:
            # Check if new name exists
            if await org_coll.find_one({"organization_name": data.organization_name}):
                raise HTTPException(status_code=400, detail="New Organization name already exists")
            
            # MIGRATION LOGIC
            old_coll_name = f"org_{current_org_name}"
            new_coll_name = f"org_{data.organization_name}"
            
            # Rename collection
            # Note: MongoDB renameCollection command usually requires admin privileges or special handling in sharded clusters.
            # Here we assume standalone/replica set.
            # Using raw command or aggregation $out (if copy needed). Rename is fastest.
            try:
                await master_db[old_coll_name].rename(new_coll_name)
            except Exception as e:
                # If old collection doesn't exist or other error
                print(f"Error renaming collection: {e}")
                # Fallback: Just create new one?
                pass
            
            collection_name = new_coll_name
        else:
            collection_name = f"org_{current_org_name}"

        # 2. Update Metadata
        hashed_password = get_password_hash(data.password)
        
        update_data = {
            "organization_name": data.organization_name, # Updated name
            "email": data.email,
            "password": hashed_password,
            "collection_name": collection_name
        }
        
        await org_coll.update_one(
            {"organization_name": current_org_name},
            {"$set": update_data}
        )
        
        updated_org = await org_coll.find_one({"organization_name": data.organization_name})
        updated_org["_id"] = str(updated_org["_id"])
        return updated_org

    @staticmethod
    async def delete_organization(org_name: str):
        master_db = db.get_master_db()
        org_coll = master_db["organizations"]
        
        # 1. Delete Metadata
        await org_coll.delete_one({"organization_name": org_name})
        
        # 2. Drop Collection
        coll_name = f"org_{org_name}"
        await master_db.drop_collection(coll_name)
        
        return True
