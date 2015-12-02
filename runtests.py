import sys
import os
import django
from django.conf import settings
from django.core.management import call_command

opts = {
    'INSTALLED_APPS': ['goodforms'],
    'TEMPLATES': [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
    }],
    'TEMPLATE_DEBUG': True,
}

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
settings.configure(**opts)
django.setup()

if __name__ == '__main__':
    call_command('test', 'goodforms')
