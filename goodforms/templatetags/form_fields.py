from collections import OrderedDict, Iterable
from django.forms.forms import BoundField
from django.template import Library
from goodforms.html import HtmlTags
from django.conf import settings

tags = HtmlTags(xhtml=settings.GOODFORMS_XHTML)
register = Library()


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

    if isinstance(field, BoundField):
        attrs['name'] = field.name
        if settings.GOODFORMS_AUTO_ID:
            attrs.setdefault('id', 'field_' + field.name)

        if 'value' not in attrs:
            field_value = field.value()
            attrs['value'] = field_value if field_value not in [False, None] else ''

        if 'required' not in attrs:
            attrs['required'] = field.field.required

    elif isinstance(field, str):
        attrs['name'] = field
        if settings.GOODFORMS_AUTO_ID:
            attrs.setdefault('id', settings.GOODFORMS_ID_PREFIX + field)

    return tags.input(**attrs)


@register.simple_tag
def textarea(field, value=None, **attrs):
    if isinstance(field, BoundField):
        attrs['name'] = field.name
        if settings.GOODFORMS_AUTO_ID:
            attrs.setdefault('id', settings.GOODFORMS_ID_PREFIX + field.name)

        if not value:
            value = field.value()

        if 'required' not in attrs:
            attrs['required'] = field.field.required

    elif isinstance(field, str):
        attrs['name'] = field
        if settings.GOODFORMS_AUTO_ID:
            attrs.setdefault('id', settings.GOODFORMS_ID_PREFIX + field)

    return tags.textarea(value, **attrs)


@register.simple_tag
def checkbox(field, label, **attrs):
    attrs.setdefault('type', 'checkbox')

    if isinstance(field, BoundField):
        attrs['name'] = field.name
        if settings.GOODFORMS_AUTO_ID:
            attrs.setdefault('id', settings.GOODFORMS_ID_PREFIX + field.name)
        if 'value' in attrs:
            attrs['checked'] = (field.value() == attrs['value'])

    elif isinstance(field, str):
        attrs['name'] = field
        if settings.GOODFORMS_AUTO_ID:
            attrs.setdefault('id', settings.GOODFORMS_ID_PREFIX + field)

    if not label:
        return tags.input(**attrs)

    input_attrs_keys = ['value', 'name', 'type', 'checked', 'id']
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
def select(field, values, value_key=None, label_key=None, **attrs):
    placeholder = attrs.get('placeholder')
    select_value = attrs.get('value')
    options_html = ''

    if placeholder:
        options_html += tags.option(placeholder, value='')

    def attr(option, key):
        if isinstance(option, dict):
            option_value = option.get(key)
        else:
            option_value = getattr(option, key)

        if hasattr(option_value, '__call__'):
            option_value = option_value()

        return option_value

    if isinstance(field, BoundField):
        attrs['name'] = field.name
        select_value = attrs.get('value', field.value())
        if settings.GOODFORMS_AUTO_ID:
            attrs.setdefault('id', settings.GOODFORMS_ID_PREFIX + field.name)

    elif isinstance(field, str):
        attrs['name'] = field
        if settings.GOODFORMS_AUTO_ID:
            attrs.setdefault('id', settings.GOODFORMS_ID_PREFIX + field)

    if isinstance(values, str):
        for option_value, option_label in parse_values(values).items():
            selected = option_value == str(select_value)
            options_html += tags.option(option_label, value=option_value, selected=selected)

    elif isinstance(values, dict):
        for option_value, option_label in values.items():
            if value_key:
                option_value = attr(option_value, value_key)
            if label_key:
                option_label = attr(option_value, label_key)

            selected = str(select_value) == str(option_value)
            options_html += tags.option(option_label, value=option_value, selected=selected)

    elif isinstance(values, Iterable):
        if not value_key:
            value_key = 'id'
        if not label_key:
            label_key = 'name'

        for value in values:
            option_value = attr(value, value_key)
            option_label = attr(value, label_key)

            selected = str(select_value) == str(option_value)
            options_html += tags.option(option_label, value=option_value, selected=selected)

    return tags.select(options_html, **attrs)


@register.simple_tag
def label(field, content='', **attrs):
    if isinstance(field, BoundField):
        if settings.GOODFORMS_AUTO_ID:
            attrs['for'] = settings.GOODFORMS_ID_PREFIX + field.name
        if not content:
            content = field.label

    elif isinstance(field, str):
        attrs['for'] = settings.GOODFORMS_ID_PREFIX + field

    return tags.label(content, **attrs)


@register.simple_tag
def submit_button(label='Submit', **attrs):
    attrs.setdefault('type', 'submit')
    return tags.button(label, **attrs)
