from celery import Celery
from app.core.config import settings


celery = Celery(
    "document_pipeline",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)


celery.conf.task_routes = {
    "app.tasks.pdf_tasks.*": {"queue": "pdf_queue"},
    "app.tasks.notification_tasks.*": {"queue": "notification_queue"},
}