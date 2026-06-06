from celery import Celery
from app.core.config import settings


celery = Celery(
    "document_pipeline",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.pdf_task",
        "app.tasks.notification_task"
    ]
)


celery.conf.task_routes = {
    "app.tasks.pdf_task.*": {"queue": "pdf_queue"},
    "app.tasks.notification_task.*": {"queue": "notification_queue"},
}