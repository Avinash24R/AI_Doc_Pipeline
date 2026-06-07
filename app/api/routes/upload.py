import os

from fastapi import APIRouter, UploadFile, File, Depends, Form , HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Document

from app.services.s3_service import upload_file_s3

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
        raise HTTPException(
            status_code=400,
            detail= "Invalid filename"
        )

    s3 = upload_file_s3(file)
    document = Document(
        filename=file.filename,
        s3_key=s3["s3_key"],
        s3_url=s3["s3_url"],
        status="PENDING",
        user_email=email
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