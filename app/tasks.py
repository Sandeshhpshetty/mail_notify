from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email: str, username: str = ""):
    subject = "Welcome to MySite!"
    message = f"Hi {username or 'there'},\n\nThanks for signing up!"
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")
    send_mail(subject, message, from_email, [user_email], fail_silently=False)
    return {"to": user_email}
