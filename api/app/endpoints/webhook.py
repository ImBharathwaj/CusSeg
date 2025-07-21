from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.crud import store_webhook_event, log_audit

router = APIRouter()

@router.post("/webhook/{client_id}")
async def receive_webhook(client_id: str, request: Request, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    payload = await request.json()
    event = store_webhook_event(db, client_id, current_user, payload)
    log_audit(db, user=current_user, action="webhook", resource=client_id, status="success", detail={"payload": payload})
    return {"status": "received", "client": client_id, "event_id": event.id}
