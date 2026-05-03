from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django_rq import job

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
        'dashboard_url': 'https://knowflow.moises.tech/dashboard',
    }

    # Render templates
    html_content = render_to_string('emails/welcome.html', context)
    text_content = render_to_string('emails/welcome.txt', context)

    # Create email
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    
    msg.send()

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
    msg.send()
