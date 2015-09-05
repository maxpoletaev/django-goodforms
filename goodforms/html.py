def render_attrs(attrs, exclude=[]):
    result = []
    is_true = ['true']
    is_false = ['false', 'none', 'null']

    for key, value in attrs.items():
        key = key.replace('_', '-')

        if key not in exclude:
            if type(value) == bool:
                if value:
                    result.append(key)
            else:
                if type(value) !=  str:
                    value = str(value)
                if value.lower() in is_true:
                    result.append(key)
                if value.lower() not in is_false:
                    result.append('%s="%s"' % (key, value))

    return ' '.join(result)


def render_tag(tag, content=None, closeable=False, **attrs):
    html = '<%s %s>' % (tag, render_attrs(attrs))

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

    def __getattr__(self, tag_name):
        def wrapper(content=None, **attrs):
            merged_attrs = {}
            if tag_name in self.tags_preset:
                merged_attrs = self.tags_preset[tag_name]
            merged_attrs.update(attrs)
            return render_tag(tag_name, content, **merged_attrs)
        return wrapper


tags = HtmlTags()
