from app.core.celery_app import celery

from app.db.database import SessionLocal
from app.db.models import Document

from app.services.pdf_service import extract_text_from_pdf
from app.services.ai_service import generate_summary

from app.tasks.notification_task import send_completion_email


@celery.task(name="process_pdf")
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

        text = extract_text_from_pdf(document.filepath)

        summary = generate_summary(text)

        document.extracted_text = text
        document.summary = summary
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

        print(str(e))

    finally:
        db.close()