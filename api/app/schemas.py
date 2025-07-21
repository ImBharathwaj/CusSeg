from pydantic import BaseModel, EmailStr
from typing import Optional, Any, Dict

class Config:
    orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class WebhookPayload(BaseModel):
    pass

class AuditEntry(BaseModel):
    user: str
    action: str
    resource: str
    status: str
    detail: Optional[Dict]
    timestamp: str
