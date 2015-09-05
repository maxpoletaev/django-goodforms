from django.forms.forms import BoundField
from django.template import Library
from collections import OrderedDict
from goodforms.html import tags

register = Library()


def attrs_defaults(attrs, defaults):
    for key, value in defaults.items():
        attrs.setdefault(key, value)


def parse_values(values):
    rows = values.split(',')
    data = OrderedDict()

    for row in rows:
        key, value = row.strip().split(':')
        value = value.strip()
        key = key.strip()

        if value in ['None', 'null']:
            value = None
        elif value in ['True', 'true']:
            value = True
        elif value in ['False', 'false']:
            value = False

        data[key] = value

    return data


@register.simple_tag
def textfield(field, **attrs):
    attrs.setdefault('type', 'text')
    attrs['name'] = field

    if isinstance(field, BoundField):
        attrs['name'] = field.name

        if 'value' not in attrs:
            field_value = field.value()
            attrs['value'] = field_value if field_value not in [False, None] else ''

        if 'required' not in attrs:
            attrs['required'] = field.field.required

    return tags.input(**attrs)


@register.simple_tag
def textarea(field, value=None, **attrs):
    attrs['name'] = field

    if isinstance(field, BoundField):
        attrs['name'] = field.name

        if not value:
            value = field.value()

        if 'required' not in attrs:
            attrs['required'] = field.field.required

    return tags.textarea(value, **attrs)


@register.simple_tag
def checkbox(field, label, **attrs):
    attrs.setdefault('type', 'checkbox')

    if isinstance(field, BoundField):
        attrs['name'] = field.name

        if 'value' in attrs:
            attrs['checked'] = (field.value() == attrs['value'])
    else:
        attrs['name'] = field

    if not label:
        return tags.input(**attrs)

    input_attrs_keys = ['value', 'name', 'type', 'checked']
    label_attrs = attrs.copy()
    input_attrs = {}

    for key in input_attrs_keys:
        input_attrs[key] = attrs.get(key)
        del label_attrs[key]

    checkbox = tags.input(**input_attrs) + ' ' + label
    return tags.label(checkbox, **label_attrs)


@register.simple_tag
def radio(field, label=None, **attrs):
    attrs.setdefault('type', 'radio')
    return checkbox(field, label, **attrs)


@register.simple_tag
def select(field, values, value_key='id', value_label='name', **attrs):
    value = attrs.get('value', field.value())
    placeholder = attrs.get('placeholder')
    options = ''

    if placeholder:
        options += tags.option(placeholder, value='')

    if isinstance(values, str):
        for option_label, option_value in parse_values(values).items():
            selected = (option_value == str(value))
            options += tags.option(option_label, value=option_value, selected=selected)

    else:
        def attr(option, key):
            if isinstance(option, dict):
                option_value = option.get(key)
            else:
                option_value = getattr(option, key)

            if hasattr(option_value, '__call__'):
                option_value = option_value()

            return option_value

        for option in values:
            option_value = attr(option, value_key)
            option_label = attr(option, value_label)

            selected = (str(value) == str(option_value))
            options += tags.option(option_label, value=option_value, selected=selected)

    return tags.select(options, **attrs)


@register.simple_tag
def submit_button(field=None, label='Submit', value=None):
    return tags.button(label, type='submit')
