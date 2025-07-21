from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.crud import log_audit

router = APIRouter()

@router.post("/ingest")
async def ingest_event(request: Request, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    payload = await request.json()
    # (Store payload as needed)
    log_audit(db, user=current_user, action="ingest", resource="/ingest", status="success", detail={"payload": payload})
    return {"status": "received"}
