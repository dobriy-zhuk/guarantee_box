"""
WSGI config for guarantee project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

#путь к проекту
sys.path.append('/home/distant_box/public_html')
#путь к фреймворку
sys.path.append('/home/distant_box/Distant/')
#путь к виртуальному окружению
sys.path.append('/home/distant_box/.venv/lib64/python3.8/site-packages/')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guarantee.settings')
#os.environ('DJANGO_SETTINGS_MODULE', 'guarantee.settings')

application = get_wsgi_application()


