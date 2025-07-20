from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean
from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class IngestPayload(BaseModel):
    customer_id: str = Field(..., description = "Unique identifier of customer")
    attributes: Optional[Dict[str, str]] = None
    source: Optional[str] = None
    timestamp: Optional[str] = None

class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True)
    user = Column(String)
    payload = Column(JSON)
    received_at = Column(DateTime, default=datetime.utcnow)

class AccessTokenSession(Base):
    __tablename__ = "access_token_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    token = Column(String, unique=True, index=True)  # Store the actual JWT token string
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    user_agent = Column(String, nullable=True)       # Optionally track device
    revoked = Column(Boolean, default=False)