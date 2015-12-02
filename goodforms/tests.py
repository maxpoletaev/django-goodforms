from django.template import Template, Context
from htmlutils import parse_attrs
from unittest import TestCase
from django import forms
import re


def render_template(content, form=None, **context_args):
    tpl = Template('{% load form_fields %} ' + content)
    context_args['form'] = form
    context = Context(context_args)
    return tpl.render(context)


def parse_html_tag(html, closeable=False):
    regex = r'<([a-z]+)\s?([^<]*)>'

    if closeable:
        regex += r'(.*)</([^>]*)>'
        match = re.search(regex, html)
        return match.group(1), parse_attrs(match.group(2)), match.group(3)

    match = re.search(regex, html)
    return match.group(1), parse_attrs(match.group(2))


def parse_html_options(html):
    option_re = re.compile(r'<option\s?([^<]*)>([^>]*)</option>')
    options = []

    for line in split_tags(html):
        match = option_re.search(line)

        if match:
            options.append({
                'attrs': parse_attrs(match.group(1), order=False),
                'content': match.group(2),
            })

    return options


def split_tags(lines):
    lines = lines.split('><')
    lines_count = len(lines) - 1
    result = []

    for i, line in enumerate(lines):
        if i == 0:
            tpl = '{}>'
        elif i == lines_count:
            tpl = '<{}'
        else:
            tpl = '<{}>'

        result.append(tpl.format(line))
    return result


class MyForm(forms.Form):
    username = forms.CharField()
    i_agree = forms.BooleanField()
    country = forms.ChoiceField(
        choices=(('ru', 'Russia'), ('us', 'United States'))
    )


class FormFieldsTest(TestCase):
    def setUp(self):
        self.form = MyForm()

    def assertInDict(self, a, b):
        self.assertTrue(
            all(a.get(k) == v for k, v in b.items()),
            '{} not in {}'.format(str(a), str(b)),
        )

    def assertInList(self, a, b):
        for item in a:
            self.assertTrue(item in b, '{} not in {}'.format(str(a), str(b)))

    def test_textfield(self):
        form = MyForm(initial={'username': 'John'})
        tag, attrs = parse_html_tag(render_template('{% textfield form.username attr="value" %}', form))
        expect_attrs = dict(id='field_username', type='text', name='username', value='John', attr='value', required=True)
        self.assertEqual(tag, 'input')
        self.assertInDict(attrs, expect_attrs)

    def test_textarea(self):
        form = MyForm()
        tag, attrs = parse_html_tag(render_template('{% textarea form.username attr="value" %}', form))
        expect_attrs = dict(id='field_username', name='username', attr='value')
        self.assertEqual(tag, 'textarea')
        self.assertInDict(attrs, expect_attrs)

    def test_checkbox(self):
        form = MyForm()
        tag, attrs = parse_html_tag(render_template('{% checkbox form.i_agree %}', form))
        expect_attrs = dict(type='checkbox', name='i_agree', value='true')
        self.assertEqual(tag, 'input')
        self.assertInDict(attrs, expect_attrs)

    def test_select(self):
        form = MyForm(initial={'country': 'ru'})
        html = render_template('{% select form.country %}', form)

        tag, attrs, content = parse_html_tag(html, closeable=True)
        self.assertEqual(tag, 'select')

        self.assertEqual(parse_html_options(content), [
            {'attrs': {'value': 'ru', 'selected': True}, 'content': 'Russia'},
            {'attrs': {'value': 'us'}, 'content': 'United States'},
        ])

        """Values from dict"""

        values = {'ru': 'Russia', 'us': 'United States'}
        html = render_template('{% select form.country values=values %}', form, values=values)
        options = parse_html_options(parse_html_tag(html, closeable=True)[2])

        self.assertInList(options, [
            {'attrs': {'value': 'ru', 'selected': True}, 'content': 'Russia'},
            {'attrs': {'value': 'us'}, 'content': 'United States'},
        ])

        """Values from list"""

        values = [{'code': 'ru', 'title': 'Russia'}, {'code': 'us', 'title': 'United States'}]
        html = render_template('{% select form.country values=values label_key="title" value_key="code" %}', form, values=values)
        options = parse_html_options(parse_html_tag(html, closeable=True)[2])

        self.assertEqual(options, [
            {'attrs': {'value': 'ru', 'selected': True}, 'content': 'Russia'},
            {'attrs': {'value': 'us'}, 'content': 'United States'},
        ])

        """Values from list of tuples"""

        values = [('ru', 'Russia'), ('us', 'United States')]
        html = render_template('{% select form.country values=values %}', form, values=values)
        options = parse_html_options(parse_html_tag(html, closeable=True)[2])

        self.assertEqual(options, [
            {'attrs': {'value': 'ru', 'selected': True}, 'content': 'Russia'},
            {'attrs': {'value': 'us'}, 'content': 'United States'},
        ])

        """Values from string"""

        values = 'ru: Russia, us: United States'
        html = render_template('{% select form.country values=values %}', form, values=values)
        options = parse_html_options(parse_html_tag(html, closeable=True)[2])

        self.assertEqual(options, [
            {'attrs': {'value': 'ru', 'selected': True}, 'content': 'Russia'},
            {'attrs': {'value': 'us'}, 'content': 'United States'},
        ])
