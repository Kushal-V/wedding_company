from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None

    async def connect_to_database(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        print("Connected to MongoDB")

    async def close_database_connection(self):
        if self.client:
            self.client.close()
            print("Closed MongoDB connection")

    def get_master_db(self):
        return self.client[settings.MASTER_DB_NAME]

    def get_org_db(self, org_name: str):
         # In our dynamic collection design, we likely use the SAME DB as master
         # but different collections. If using separate DBs, change this.
         # For this assignment, "dynamic collections" implies same DB unless specified.
         # The requirement says "Dynamically create a new collection".
         # So we use master DB? Or a separate "tenants" DB?
         # "Programmatically create new Mongo collections for each organization"
         # Master DB used for metadata.
         # We will use the SAME database `master_db` for simplicity and Atlas limits (free tier is 1 cluster).
         return self.client[settings.MASTER_DB_NAME]

db = Database()
