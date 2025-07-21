from app.models import User, AuditLog, WebhookEvent, AccessTokenSession
from datetime import datetime

def log_audit(db, user, action, resource, status, detail=None):
    entry = AuditLog(
        user=user,
        action=action,
        resource=resource,
        status=status,
        detail=detail,
        timestamp=datetime.utcnow()
    )
    db.add(entry)
    db.commit()

def store_webhook_event(db, client_id, user, payload):
    event = WebhookEvent(
        client_id=client_id,
        user=user,
        payload=payload,
        received_at=datetime.utcnow()
    )
    db.add(event)
    db.commit()
    return event