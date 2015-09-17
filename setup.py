from setuptools import setup, find_packages

setup(
    name='django-goodforms',
    version='0.1.0',
    description='Custom renderer for your form fields',
    long_description=open('README.rst').read(),
    author='Maxim Poletaev',
    author_email='zenwalker2@gmail.com',
    url='https://github.com/zenwalker/django-goodforms',
    packages=['goodforms', 'goodforms.templatetags'],
)
