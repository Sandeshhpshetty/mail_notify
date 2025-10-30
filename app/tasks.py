# app/tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = get_task_logger(__name__)

@shared_task(bind=True, name='emails.send_welcome_email', queue='emails', max_retries=3)
def send_welcome_email(self, user_id, email, username):
    """
    Sends a welcome email using SMTP. Uses an HTML template + plain text fallback.
    """
    try:
        subject = "Welcome back to OurSite!"
        # render html body from template (app/templates/html/email_template.html)
        html_body = render_to_string('html/email_template.html', {'username': username})
        text_body = f"Hi {username},\n\nWelcome back to OurSite!\n\n— The Team"

        msg = EmailMultiAlternatives(subject=subject, body=text_body,
                                     from_email=settings.DEFAULT_FROM_EMAIL,
                                     to=[email])
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)

        logger.info("Welcome email sent to %s (user_id=%s)", email, user_id)
        return {"status": "sent", "user_id": user_id}
    except Exception as exc:
        logger.exception("Failed to send welcome email to %s", email)
        # retry with backoff
        raise self.retry(exc=exc, countdown=10)
