from setuptools import setup

setup(
    name='django-goodforms',
    version='0.1.0',
    description='Custom renderer for django form fields',
    keywords='django forms',
    author='Maxim Poletaev',
    author_email='zenwalker2@gmail.com',
    license='BSD',
    url='https://github.com/zenwalker/django-goodforms',
    packages=['goodforms', 'goodforms.templatetags'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
    ],
)
