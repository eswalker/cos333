"""
WSGI config for rowsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
from django.core.wsgi import get_wsgi_application
import os

"""
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rowsite.dev")
application = get_wsgi_application()"""

# For Production
from dj_static import Cling
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rowsite.settings")
application = Cling(get_wsgi_application())