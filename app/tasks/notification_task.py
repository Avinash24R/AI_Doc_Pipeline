from app.core.celery_app import celery

from app.services.email_service import send_email


@celery.task(bind=True, max_retries=3, name="app.tasks.notification_task.send_completion_email")
def send_completion_email(
    self,
    user_email: str,
    filename: str
):

    try:

        send_email(
            to_email=user_email,
            subject="Document Processing Completed",
            body=f"{filename} has been processed successfully."
        )

    except Exception as e:

        raise self.retry(exc=e, countdown=60)