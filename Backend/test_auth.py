import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()
from django.contrib.auth import authenticate
user = authenticate(username="moi", password="1234")
if user:
    print("USER MOI EXISTS AND PASSWORD IS CORRECT!")
else:
    print("USER MOI IS INVALID OR PASSWORD IS INCORRECT!")
