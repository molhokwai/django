'\nASGI config for django_app project.\n\nIt exposes the ASGI callable as a module-level variable named ``application``.\n\nFor more information on this file, see\nhttps://docs.djangoproject.com/en/4.2/howto/deployment/asgi/\n'
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_app.settings')
application=get_asgi_application()