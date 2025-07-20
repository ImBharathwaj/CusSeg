from fastapi import FastAPI, UploadFile, File, Request, Header, HTTPException
from minio import Minio
from hdfs import InsecureClient
import logging
import io
import os
from datetime import datetime, timedelta
from app.auth import is_valid_api_key, create_access_token, get_current_user
from app.storage.base import StorageHandler
from app.storage.minio_handler import MinioStorageHandler
from app.storage.hdfs_handler import HDFSStorageHandler
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Base, IngestPayload, WebhookEvent, AccessTokenSession
from app.schemas import UserCreate, UserOut
from app.database import engine, get_db
from sqlalchemy.future import select
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

SECRET_KEY = "YOUR_SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
API_KEYS = set(os.getenv("API_KEYS", "").split(","))

minio_client = Minio(
    "localhost:9000",
    access_key = "minioadmin",
    secret_key = "minioadmin",
    secure = False
)

minio_handler = MinioStorageHandler(bucket="cusseg-demo-bucket", client=minio_client)

hdfs_client = InsecureClient('http://localhost:50070', user='hadoop')
hdfs_handler = HDFSStorageHandler(base_path="/user/hadoop", client=hdfs_client)

def require_api_key(x_api_key: str = Header(...)):
    if not is_valid_api_key(x_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )

def get_handler(storage_type: str):
    if storage_type == "minio":
        return minio_handler
    elif storage_type == "hdfs":
        return hdfs_handler
    else:
        raise ValueError("Unsupported storage type")

async def authenticate_user(username: str, password: str, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user


# Create DB tables at startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/users", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if username or email already exists
    result = await db.execute(select(User).where(User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    audit = AuditLog(
        user=current_user,
        action="upload",
        resource=file.filename,
        status="success",
        detail={"size": file.size}
    )
    db.add(audit)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    # access_token = create_access_token(data={"sub": user.username})
    # return {"access_token": access_token, "token_type": "bearer"}

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    session = AccessTokenSession(
        user_id=user.id,
        token=access_token,
        issued_at=datetime.utcnow(),
        expires_at=expire,
        user_agent=form_data.scopes[0] if form_data.scopes else None  # Or parse from Request
    )
    audit = AuditLog(
        user=current_user,
        action="upload",
        resource=file.filename,
        status="success",
        detail={"size": file.size}
    )
    db.add(audit)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Configure logging
logging.basicConfig(
    filename='webhook_events.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger("webhook_logger")


@app.get('/')
def home():
    return "Home"

@app.get("/health")
def health_check():
    return {"status":"ok"}


@app.post("/ingest")
def ingestion(payload: IngestPayload):
    print(payload)
    return {"message": "Ingestion successful", "data": payload.model_dump()}


@app.post('/upload')
async def upload_file(
    file: UploadFile = File(...),
    storage: str = "minio",
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    content = await file.read()
    handler = get_handler(storage)
    audit = AuditLog(
        user=current_user,
        action="upload",
        resource=file.filename,
        status="success",
        detail={"size": file.size}
    )
    db.add(audit)
    handler.save(file.filename, content)
    return {"filename": file.filename, "stored_id": storage}

@app.post("/webhook")
async def receive_webhook(request: Request):
    payload = await request.json()
    print(f"Received webhook event: {payload}")
    logger.info(f"Received webhook: {payload}")
    return {"status": "received"}


@app.post("/webhook/{client_id}")
async def receive_webhook(client_id: str,
                        request: Request,
                        current_user: str = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)
                        ):
    payload = await request.json()
    event = WebhookEvent(
        client_id=client_id,
        user=current_user,
        payload=payload,
        received_at=datetime.utcnow()
    )
    audit = AuditLog(
        user=current_user,
        action="upload",
        resource=file.filename,
        status="success",
        detail={"size": file.size}
    )
    db.add(audit)
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return {"status": "received", "client": client_id, "event_id": event.id}
    logger.info(f"{datetime.utcnow().isoformat()} | {current_user} | {client_id} | {payload}\n")
