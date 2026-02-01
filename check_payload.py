#!/usr/bin/env python3
import os, sys
os.chdir('/app/P1')
sys.path.insert(0, '/app/P1')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from pyas2.models import Message

msg = Message.objects.get(id=1)
print('Payload type:', type(msg.payload))
print('Payload length:', len(msg.payload) if msg.payload else 0)
if msg.payload:
    if isinstance(msg.payload, bytes):
        print('Payload (decoded):', msg.payload.decode('utf-8', errors='replace')[:500])
    else:
        print('Payload:', str(msg.payload)[:500])
