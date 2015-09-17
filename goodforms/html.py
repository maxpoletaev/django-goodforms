def render_attrs(attrs, xhtml=False, exclude=[]):
    result = []
    is_true = ['true']
    is_false = ['false', 'none', 'null']

    for key, value in attrs.items():
        key = key.replace('_', '-')

        if key not in exclude:
            if type(value) == bool:
                if value:
                    if xhtml:
                        result.append('%s="%s"' % (key, key))
                    else:
                        result.append(key)
            else:
                if type(value) !=  str:
                    value = str(value)

                if value.lower() in is_true:
                    if xhtml:
                        result.append('%s="%s"' % (key, key))
                    else:
                        result.append(key)

                if value.lower() not in is_false:
                    result.append('%s="%s"' % (key, value))

    return ' '.join(result)


def render_tag(tag, content=None, closeable=False, xhtml=False, **attrs):
    attrs = render_attrs(attrs, xhtml=xhtml)
    html = '<' + tag

    if attrs:
        html += ' ' + attrs

    html += ' />' if xhtml and not (content or closeable) else '>'

    if content:
        html += content

    if content or closeable:
        html += '</%s>' % tag

    return html


class HtmlTags:
    tags_preset = {
        'button': {'closeable': True},
        'textarea': {'closeable': True}
    }

    def __init__(self, xhtml=False):
        self.xhtml = xhtml

    def __getattr__(self, tag_name):
        def wrapper(content=None, **attrs):
            merged_attrs = {}
            if tag_name in self.tags_preset:
                merged_attrs = self.tags_preset[tag_name]
            merged_attrs.update(attrs)
            return render_tag(tag_name, content, xhtml=self.xhtml, **merged_attrs)
        return wrapper
