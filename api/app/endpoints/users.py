from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserCreate, Token
from app.models import User, AccessTokenSession
from app.database import get_db
from app.auth import get_password_hash, authenticate_user, create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/users")
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=409, detail="Username exists")
    hashed_password = get_password_hash(user_in.password)
    user_obj = User(username=user_in.username, email=user_in.email, hashed_password=hashed_password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return {"username": user_obj.username, "email": user_obj.email}

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    session = AccessTokenSession(
        user_id=user.id,
        token=access_token,
        issued_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(minutes=30)
    )
    db.add(session)
    db.commit()
    return {"access_token": access_token, "token_type": "bearer"}
