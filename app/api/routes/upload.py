import os
import uuid
import aiofiles
from fastapi import APIRouter, UploadFile, File, Depends, Form

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Document

from app.core.config import settings

from app.tasks.pdf_task import process_pdf

from datetime import datetime , timezone

router = APIRouter()


@router.post("/upload")
async def upload_pdf(
    email: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise ValueError("Invalid filename")
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(
        settings.UPLOAD_DIR,
        filename
    )

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await file.read())

    document = Document(
        filename=file.filename,
        filepath=file_path,
        user_email=email,
        queued_at=datetime.now(timezone.utc)
    )

    db.add(document)
    db.commit()
    db.refresh(document)
    print("Queueing Task")
    process_pdf.delay(# pyright: ignore[reportFunctionMemberAccess]
        document.id
        )
    print("Task Queued")
    return {
        "message": "PDF uploaded successfully",
        "document_id": document.id,
        "status": "PENDING"
    }