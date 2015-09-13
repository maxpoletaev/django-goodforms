from django.conf import settings

default_settings = {
    'GOODFORMS_XHTML': False,
}

def setup():
    for key, value in default_settings.items():
        if not hasattr(settings, key):
            setattr(settings, key, value)
