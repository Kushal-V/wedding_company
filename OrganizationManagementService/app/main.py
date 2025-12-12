from fastapi import FastAPI
from app.core.database import db
from app.routers import auth, organization

app = FastAPI(title="Organization Management Service")

@app.on_event("startup")
async def startup_db_client():
    db.connect_to_database()

@app.on_event("shutdown")
async def shutdown_db_client():
    db.close_database_connection()

app.include_router(organization.router, prefix="/org", tags=["organization"])
app.include_router(auth.router, prefix="/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Backend Intern Assignment API is running"}
