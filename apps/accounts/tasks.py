from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_account_activated_email(user_email, username):
    subject = 'Your Airbooking Account is Activated'
    message = (
        f'Hello {username},\n\n'
        'Your Airbooking account has been approved and activated by an administrator. '
        'You can now log in and start booking flights.\n\n'
        'Thank you,\nAirbooking Team'
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )