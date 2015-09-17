from django.conf import settings

default_settings = {
    'XHTML': False,
    'AUTO_ID': True,
    'ID_PREFIX': 'field_',
}

def setup():
    for key, value in default_settings.items():
        rkey = 'GOODFORMS_' + key
        if not hasattr(settings, rkey):
            setattr(settings, rkey, value)
