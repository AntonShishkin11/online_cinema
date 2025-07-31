
import os
import logging
from celery.utils.log import get_task_logger
from celery.exceptions import Retry
from app.core.celery import celery_app
from app.services.mailer import send_email, render_template

logger = get_task_logger(__name__)

@celery_app.task(
    name="app.tasks.send_email_task",
    bind=True,
    autoretry_for=(Exception,),
    max_retries=5,
    retry_backoff=True,
    retry_jitter=True,
)
def send_email_task(self, to_email: str, subject: str, email_type: str, token: str):
    try:
        if email_type == "verify":
            verify_url = os.getenv("VERIFY_EMAIL_URL", "#")
            html = render_template("email/verify_email.html", {
                "verify_link": f"{verify_url}?token={token}"
            })
        elif email_type == "reset":
            reset_url = os.getenv("RESET_PASSWORD_URL", "#")
            html = render_template("email/reset_password.html", {
                "reset_link": f"{reset_url}?token={token}"
            })
        else:
            logger.error(f"Unknown email_type: {email_type}")
            raise ValueError(f"Unknown email_type: {email_type}")

        send_email(to_email, subject, html)
        logger.info(f"Email sent to {to_email} with type {email_type}")

    except Exception as e:
        logger.exception(f"Failed to send email to {to_email}: {str(e)}")
        raise self.retry(exc=e)
