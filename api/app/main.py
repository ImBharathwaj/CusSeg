from fastapi import FastAPI
from app.endpoints import users, upload, ingest, webhook  # Import all routers
from app.database import Base, engine

# (Optional) Create all tables on startup for dev/demo
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers for clear modular endpoints
app.include_router(users.router)
app.include_router(upload.router)
app.include_router(ingest.router)
app.include_router(webhook.router)
# app.include_router(audit.router)  # Optional: for viewing audit logs

@app.get("/health")
async def health():
    return {"status": "ok"}
