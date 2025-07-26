from app.core.celery import celery_app

def send_email_async(to_email: str, subject: str, email_type: str, token: str):
    celery_app.send_task(
        "app.tasks.send_email_task",
        args=[to_email, subject, email_type, token],
        queue="emails"
    )
