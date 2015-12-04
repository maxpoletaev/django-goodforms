import sys
import os
import django
from django.conf import settings
from django.conf.urls import url
from django.core.management import call_command

urlpatterns = [
    url(r'^actions/form-action$', lambda: 'ok', name='form_action'),
]

opts = {
    'INSTALLED_APPS': ['goodforms'],
    'ROOT_URLCONF': urlpatterns,
    'TEMPLATE_DEBUG': True,
    'TEMPLATES': [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
    }],
}

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    settings.configure(**opts)
    django.setup()

    call_command('test', 'goodforms')
