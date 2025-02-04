"""
WSGI config for cryptography_web_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Fix for Apache/mod_wsgi Python path
SITE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_PATH = os.path.join(SITE_PATH, 'venv_cryptography/lib/python3.8/site-packages')

sys.path.append(SITE_PATH)

# Add to Python path for mod_wsgi
if VENV_PATH not in sys.path:
        sys.path.append(VENV_PATH)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptography_web_app.settings')
application = get_wsgi_application()
