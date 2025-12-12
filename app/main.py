from fastapi import FastAPI
from app.core.database import db
from app.routers import auth, organization

app = FastAPI(title="Organization Management Service", version="1.0.0")

@app.on_event("startup")
async def startup_db_client():
    await db.connect_to_database()

@app.on_event("shutdown")
async def shutdown_db_client():
    await db.close_database_connection()

app.include_router(auth.router, prefix="/admin", tags=["Authentication"])
app.include_router(organization.router, prefix="/org", tags=["Organizations"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Organization Management Service"}
