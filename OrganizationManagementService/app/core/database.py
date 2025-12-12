from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None

    def connect_to_database(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        print("Connected to MongoDB")

    def close_database_connection(self):
        self.client.close()
        print("Closed MongoDB connection")

    def get_master_db(self):
        return self.client[settings.MASTER_DB_NAME]

    def get_dynamic_collection(self, org_name: str):
        # We store dynamic collections in the same database instance but could differ.
        # Requirement: "The system should maintain a Master Database... and create dynamic collections for each organization"
        # We will use the master DB connection for simplicity to access other DBs/Collections or assume they are in the same cluster.
        # The requirement implies "create dynamic collections", often in Mongo this means `db.create_collection`.
        # We'll use a naming convention for the collection: `org_{org_name}` 
        # Requirement: "Example collection name pattern: org_<organization_name>"
        
        # NOTE: Is "dynamic collection" inside the SAME DB or DIFFERENT DB? 
        # "maintain a Master Database... and create dynamic collections"
        # Usually "Collection" implies same DB. "Database" implies different DB.
        # The requirement says "create dynamic collections for each organization".
        # So we will put them in the SAME DB or a dedicated 'OrganizationsDB'.
        # Let's keep them in the `MASTER_DB_NAME` or `organizations_db`. 
        # However, separation of concerns might suggest a different DB name for tenant data.
        # Let's stick effectively to: `db['org_' + name]`.  Which DB?
        # Let's use `master_db` for metadata and `orgs_data_db` for tenant collections, OR just put everything in `master_db`.
        # To be cleanest: metadata in `master_db`, tenant data in `master_db` (or a separate one).
        # Let's use `master_db` for everything for simplicity unless specified otherwise.
        
        return self.client[settings.MASTER_DB_NAME][f"org_{org_name}"]

db = Database()
