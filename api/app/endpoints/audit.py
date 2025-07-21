from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import AuditLog

router = APIRouter()

@router.get("/audit")
def list_audit_logs(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    # (Optionally restrict to admin users)
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
