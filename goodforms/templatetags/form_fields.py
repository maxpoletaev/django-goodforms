from django.template import Library, Node
from django.template.base import token_kwargs
from collections import OrderedDict, Iterable
from django.forms.forms import BoundField
from django.utils.html import mark_safe
from htmlutils.html import HtmlTags
from django.conf import settings

tags = HtmlTags(xhtml=settings.GOODFORMS_XHTML)
register = Library()


@register.simple_tag(takes_context=True)
def textfield(context, field, **attrs):
    attrs.setdefault('type', 'text')

    if isinstance(field, BoundField):
        attrs['name'] = field.name

        if 'value' not in attrs:
            field_value = field.value()
            attrs['value'] = field_value if field_value not in [False, None] else ''

        if 'required' not in attrs:
            attrs['required'] = field.field.required

    elif isinstance(field, str):
        attrs['name'] = field

    attrs.setdefault('id', get_field_id(context, attrs.get('name')))
    return mark_safe(tags.input(**attrs))


@register.simple_tag(takes_context=True)
def textarea(context, field, value=None, **attrs):
    if isinstance(field, BoundField):
        attrs['name'] = field.name

        if not value:
            value = field.value()
        if 'required' not in attrs:
            attrs['required'] = field.field.required

    elif isinstance(field, str):
        attrs['name'] = field

    attrs.setdefault('id', get_field_id(context, attrs.get('name')))
    return mark_safe(tags.textarea(value, **attrs))


@register.simple_tag(takes_context=True)
def checkbox(context, field, label=None, **attrs):
    attrs.setdefault('type', 'checkbox')
    attrs.setdefault('value', 'true')
    return checkbox_or_radio(context, field, label, **attrs)


@register.simple_tag(takes_context=True)
def radio(context, field, label=None, **attrs):
    attrs.setdefault('type', 'radio')
    return checkbox_or_radio(context, field, label, **attrs)


def checkbox_or_radio(context, field, label=None, **attrs):
    if isinstance(field, BoundField):
        attrs['name'] = field.name

        if 'value' in attrs:
            attrs['checked'] = (field.value() == attrs['value'])

    elif isinstance(field, str):
        attrs['name'] = field

    if not label:
        attrs.setdefault('id', get_field_id(context, attrs.get('name')))
        return mark_safe(tags.input(**attrs))

    input_attrs_keys = ['value', 'name', 'type', 'checked', 'id']
    label_attrs = attrs.copy()
    input_attrs = {}

    for key in input_attrs_keys:
        value = attrs.get(key)

        if value:
            input_attrs[key] = value
            del label_attrs[key]

    checkbox = tags.input(**input_attrs) + ' ' + tags.span(label)
    return mark_safe(tags.label(checkbox, **label_attrs))


@register.simple_tag(takes_context=True)
def select(context, field, values=None, value_key=None, label_key=None, **attrs):
    placeholder = attrs.get('placeholder')
    select_value = attrs.get('value')
    options_html = ''

    if placeholder:
        options_html += tags.option(placeholder, value='')

    if isinstance(field, BoundField):
        attrs['name'] = field.name
        select_value = attrs.get('value', field.value())
        choices = getattr(field.field, 'choices', None)

        if choices and not values:
            values = choices

    elif isinstance(field, str):
        attrs['name'] = field

    if isinstance(values, str):
        for option_value, option_label in parse_values(values).items():
            selected = option_value == str(select_value)
            options_html += tags.option(option_label, value=option_value, selected=selected)

    elif isinstance(values, dict):
        for option_value, option_label in values.items():
            if value_key:
                option_value = get_attr(option_value, value_key)
            if label_key:
                option_label = get_attr(option_value, label_key)

            selected = str(select_value) == str(option_value)
            options_html += tags.option(option_label, value=option_value, selected=selected)

    elif isinstance(values, Iterable):
        if not label_key: label_key = 'name'  # noqa
        if not value_key: value_key = 'id'  # noqa

        for value in values:
            if isinstance(value, (list, tuple)):
                option_value, option_label = value
            else:
                option_label = get_attr(value, label_key)
                option_value = get_attr(value, value_key)

            selected = str(select_value) == str(option_value)
            options_html += tags.option(option_label, value=option_value, selected=selected)

    attrs.setdefault('id', get_field_id(context, attrs.get('name')))
    return mark_safe(tags.select(options_html, **attrs))


@register.simple_tag(takes_context=True)
def label(context, field, content='', **attrs):
    if isinstance(field, BoundField):
        attrs.setdefault('for', get_field_id(context, field.name))

        if not content:
            content = field.label

    return mark_safe(tags.label(content, **attrs))


@register.simple_tag
def submit_button(label='Submit', **attrs):
    attrs.setdefault('type', 'submit')
    return mark_safe(tags.button(label, **attrs))


@register.tag('form')
class FormNode(Node):
    def __init__(self, parser, token):
        self.nodelist = parser.parse(('endform', ))
        bits = token.split_contents()[1:]
        parser.delete_first_token()
        self.attrs = self.parse_attrs(bits, parser)

    def parse_attrs(self, bits, parser):
        kwargs = token_kwargs(bits, parser)
        return {k: v for k, v in kwargs.items()}

    def resolve_attrs(self, context):
        return {k: v.resolve(context) for k, v in self.attrs.items()}

    def render(self, context):
        attrs = self.resolve_attrs(context)

        context.push()
        context['FORM_NAME'] = attrs.get('name')
        output = self.nodelist.render(context)
        context.pop()

        csrf_token = context.get('csrf_token')
        if csrf_token and csrf_token != 'NOTPROVIDED':
            output += tags.input(type='hidden', name='csrfmiddlewaretoken', value=csrf_token)

        return mark_safe(tags.form(output, **attrs))


def get_attr(obj, key):
    if isinstance(obj, dict):
        option_value = obj.get(key)
    else:
        option_value = getattr(obj, key)

    if hasattr(option_value, '__call__'):
        option_value = option_value()

    return option_value


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


def get_field_id(context, field_name):
    if settings.GOODFORMS_AUTO_ID and field_name:
        prefix = context.get('FORM_NAME', settings.GOODFORMS_ID_PREFIX)
        return prefix + '_' + field_name
