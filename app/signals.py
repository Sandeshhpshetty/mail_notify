# app/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db import transaction
from .tasks import send_welcome_email

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    """
    When user logs in, enqueue welcome email task on 'emails' queue after transaction commit.
    """
    user_id = user.pk
    email = user.email
    username = user.get_username()

    # Ensure we schedule task after any DB transaction commit
    transaction.on_commit(lambda: send_welcome_email.apply_async(
        args=(user_id, email, username),
        queue='emails'
    ))
