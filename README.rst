.. image:: https://travis-ci.org/zenwalker/django-goodforms.svg
   :target: https://travis-ci.org/zenwalker/django-goodforms
   :alt: Build Status

Good forms for Django
=====================

**GoodForms** — rails-like renderer for your form fields. Provide fully control of filed styles and attributes. It's not replacement for ``django.forms``.


Installation
------------

Run ``pip install django-goodforms`` and add ``goodforms`` to ``INSTALLED_APPS``. That's all.


Usage
-----

The view::

    from django.shortcuts import render
    from django import forms

    class LoginForm(forms.Form):
        username = forms.CharField()
        password = forms.PasswordField()

    def sign_up(request):
        from = MyForm(initial={'username': 'johnsmith'})
        return render(request, 'index.html', {'form': form})


The template::

    {% load form_fields %}

    {% form name="login" class="login-form" %}
        {% textfield form.username class="login-form_input" %}
        {% textfield form.password class="login-form_input" %}
        {% submit_button "Login" %}
    {% endform %}


Controls
--------

Form tag
~~~~~~~~

- Form tag automatically inject csrf-token.
- Fields use ``name`` attribute as prefix for ``id`` and ``for`` in labels.

::

    {% form name="myform" %}
        <!-- Form content -->
    {% endform %}


Textfield and Textarea
~~~~~~~~~~~~~~~~~~~~~~

::

    {% textfield form.title **kwargs %}
    {% textarea form.description **kwargs %}


Select
~~~~~~

::

    {% select form.country values="ru:Russia,de:Germany" %}

You can use any dict, iterable collection or queryset as values list::

    {% select form.county values=any_iterable_object value_key="code" label_key="title" %}


Checkbox and radio-button
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    {% radio form.gender value="female" %}
    {% radio form.gender value="male" %}

The ``label`` attribute wraps checkbox to ``<label>`` tag. All attributes provite to it::

    {% checkbox form.agree label="I agree" style="font-weight: bold;" %}

    <label style="font-weight: bold;">
        <input type="checkbox" name="agree" value="1"> <span>I agree</span>
    </label>


Submit button
~~~~~~~~~~~~~

::

    {% submit_button "Send message" %}
    {% submit_button "Save as draft" name="is_draft" value=True %}


Tips
----

You can use any of field without a form class::

    {% input "username" required=True %}
    {% select "city" values="1:New York, 2:London" %}


Settigns
--------

``GOODFORMS_XHTML`` — Enable or disable XHTML syntax (default: ``False``)

``GOODFORMS_AUTO_ID`` — Automatically generate ``id`` and ``for`` attributes for fields and labels (default: ``True``)

``GOODFORMS_ID_PREFIX`` — Prefix for auto-generated ``id`` and ``for`` attributes. For forms without ``name`` attribute (default: ``field``)


License
-------

Licensed under the MIT license.
