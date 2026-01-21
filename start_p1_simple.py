#!/usr/bin/env python
"""
Simple P1 AS2 Server startup with SQLite
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P1.settings')

# Override database to use SQLite for quick testing
import sys
sys.path.insert(0, 'P1')
import P1.settings as settings
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'P1/p1_as2_db.sqlite3',
    }
}

django.setup()

print("Starting P1 AS2 Server on http://127.0.0.1:8000")
print("Admin: http://127.0.0.1:8000/admin/ (admin/admin123)")
print("AS2 Endpoint: http://127.0.0.1:8000/pyas2/as2receive")
print("Press Ctrl+C to stop")

from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver'])