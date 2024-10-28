"""
ASGI config for gigma project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

if os.getenv('DEV_ENV') == 'TRUE':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gigma.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gigma.settings.prod')

application = get_asgi_application()
