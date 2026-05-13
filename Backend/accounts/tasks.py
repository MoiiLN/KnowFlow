from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django_rq import job
import logging

logger = logging.getLogger(__name__)

@job
def send_welcome_email_task(username, email):
    if not email:
        return
        
    subject = '¡Bienvenido a Knowflow!'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = email

    # Context for templates
    context = {
        'username': username,
        'dashboard_url': 'http://knowflow.arkania.es/dashboard',
    }

    # Render templates
    html_content = render_to_string('emails/welcome.html', context)
    text_content = render_to_string('emails/welcome.txt', context)

    # Create email
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    
    try:
        msg.send()
        logger.info(f"Welcome email sent successfully to {email}")
    except Exception as e:
        logger.error(f"Error sending welcome email to {email}: {str(e)}")

@job
def send_goodbye_email_task(username, email):
    if not email:
        return
        
    subject = 'Esperamos verte pronto en Knowflow'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = email

    # Context for templates
    context = {
        'username': username,
    }

    # Render templates
    html_content = render_to_string('emails/goodbye.html', context)
    text_content = render_to_string('emails/goodbye.txt', context)

    # Create email
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    
    try:
        msg.send()
        logger.info(f"Goodbye email sent successfully to {email}")
    except Exception as e:
        logger.error(f"Error sending goodbye email to {email}: {str(e)}")
