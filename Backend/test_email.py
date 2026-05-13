import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
os.environ['EMAIL_BACKEND'] = 'django.core.mail.backends.smtp.EmailBackend'
django.setup()

def test_email():
    print(f"Using Backend: {settings.EMAIL_BACKEND}")
    print(f"Using Host: {settings.EMAIL_HOST}")
    print(f"Using User: {settings.EMAIL_HOST_USER}")
    
    try:
        send_mail(
            'Test Email',
            'This is a test email from Knowflow.',
            settings.DEFAULT_FROM_EMAIL,
            ['your-email@example.com'],
            fail_silently=False,
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    test_email()
