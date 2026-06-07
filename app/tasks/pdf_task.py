from app.core.celery_app import celery

from app.db.database import SessionLocal
from app.db.models import Document

from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import generate_summary
from app.services.s3_service import download_file_s3

from app.tasks.notification_task import send_completion_email
import os


@celery.task(name="app.tasks.pdf_task.process_pdf")
def process_pdf(document_id: int):

    db = SessionLocal()
    document = None

    try:

        document = db.query(Document).filter(
            Document.id == document_id
        ).first()

        if not document:
            return

        document.status = "PROCESSING"

        db.commit()

        local_path = download_file_s3(
            document.s3_key
        )
        text = extract_text_from_pdf(local_path)

        summary = generate_summary(text)

        document.extracted_text = text
        document.summary = summary
        document.status = "COMPLETED"

        db.commit()

        os.remove(local_path)
        send_completion_email.delay(# pyright: ignore[reportFunctionMemberAccess]
            document.user_email,
            document.filename,
            document.summary
        )

    except Exception as e:

        if document:
            document.status = "FAILED"
            db.commit()

        print(str(e))

    finally:
        db.close()