import sys
import os
import django
from django.conf import settings
from django.core.management import call_command

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
opts = {'INSTALLED_APPS': ['goodforms']}
settings.configure(**opts)
django.setup()

if __name__ == '__main__':
    call_command('test', 'goodforms')
