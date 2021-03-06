"""
WSGI config for PertenTime project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, sys

# Possibly a hack? Added to get the admin interface and the report to handle the Swedish specific characters. 
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('/usr/local/www/PertenTime/src')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PertenTime.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
