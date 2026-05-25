import os

from fastapi import APIRouter, UploadFile, File, Depends, Form

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Document

from app.core.config import settings

from app.tasks.pdf_task import process_pdf


router = APIRouter()


@router.post("/upload")
async def upload_pdf(
    email: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise ValueError("Invalid filename")

    file_path = os.path.join(
        settings.UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    document = Document(
        filename=file.filename,
        filepath=file_path,
        user_email=email
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    process_pdf.delay(# pyright: ignore[reportFunctionMemberAccess]
        document.id
        )

    return {
        "message": "PDF uploaded successfully",
        "document_id": document.id,
        "status": "PENDING"
    }