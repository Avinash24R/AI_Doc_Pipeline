from app.core.celery_app import celery

from app.db.database import SessionLocal
from app.db.models import Document

from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import summarize_large_document

from app.tasks.notification_task import send_completion_email

from datetime import datetime , timezone

@celery.task(bind=True ,name="app.tasks.pdf_task.process_pdf")
def process_pdf(self ,document_id: int):
    db = SessionLocal()
    document = None

    try:

        document = db.query(Document).filter(
            Document.id == document_id
        ).first()

        if not document:
            return
        document.celery_task_id = self.request.id
        start_time = datetime.now(timezone.utc)
        document.started_at = start_time
        document.status = "PROCESSING"
        if document.queued_at:
            document.queue_wait_ms = (start_time - document.queued_at).total_seconds() * 1000 
        else:
            document.queue_wait_ms = 0
        db.commit()

        text = extract_text_from_pdf(document.filepath)

        summary = text #summarize_large_document(text)

        end_time = datetime.now(timezone.utc)

        document.extracted_text = text
        document.summary = summary

        document.completed_at = end_time

        document.execution_ms = (
            end_time -
            start_time
        ).total_seconds() * 1000
        if document.queued_at:
            document.end_to_end_ms = (
                end_time -
                document.queued_at
            ).total_seconds() * 1000 
        else:
            document.end_to_end_ms = 0
        document.status = "COMPLETED"

        db.commit()


        send_completion_email.delay(# pyright: ignore[reportFunctionMemberAccess]
            document.user_email,
            document.filename
        )

    except Exception as e:

        if document:
            document.status = "FAILED"
            db.commit()

        print(f"ERROR: {e}")

    finally:
        db.close()