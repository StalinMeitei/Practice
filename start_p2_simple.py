#!/usr/bin/env python
"""
Simple P2 AS2 Server startup with SQLite
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P2.settings')

# Override database to use SQLite for quick testing
import sys
sys.path.insert(0, 'P2')
import P2.settings as settings
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'P2/p2_as2_db.sqlite3',
    }
}

django.setup()

print("Starting P2 AS2 Server on http://127.0.0.1:8001")
print("Admin: http://127.0.0.1:8001/admin/ (admin/admin123)")
print("AS2 Endpoint: http://127.0.0.1:8001/pyas2/as2receive")
print("Press Ctrl+C to stop")

from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8001'])