import os
from app.core.celery import celery_app
from app.services.mailer import send_email, render_template

@celery_app.task(name="app.tasks.send_email_task")
def send_email_task(to_email: str, subject: str, email_type: str, token: str):
    if email_type == "verify":
        verify_url = os.getenv("VERIFY_EMAIL_URL")
        html = render_template("email/verify_email.html", {
            "verify_link": f"{verify_url}?token={token}"
        })
        send_email(to_email, subject, html)

    elif email_type == "reset":
        reset_url = os.getenv("RESET_PASSWORD_URL")
        html = render_template("email/reset_password.html", {
            "reset_link": f"{reset_url}?token={token}"
        })
        send_email(to_email, subject, html)

    else:
        raise ValueError("Unknown email_type")
