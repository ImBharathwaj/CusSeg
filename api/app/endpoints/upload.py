from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.crud import log_audit

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    contents = await file.read()
    # Store file, e.g., save to disk/S3/object storage here...
    log_audit(db, user=current_user, action="upload", resource=file.filename, status="success", detail={"size": len(contents)})
    return {"filename": file.filename, "size": len(contents)}
