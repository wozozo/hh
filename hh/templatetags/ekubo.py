# coding: utf-8

from urllib import urlencode

from django import template
from django.conf import settings

register = template.Library()


class EkuboNode(template.Node):

    def __init__(self, path, params):
        self.path = template.Variable(path)
        self.params = params
        self.escape = False

    def render(self, context):

        actual_path = self.path.resolve(context)
        path = _get_path(actual_path)
        url = 'http://{}/{}'.format(settings.EKUBO_DOMAIN, path)

        return url + self.buildquery()

    def buildquery(self):

        if not len(self.params):
            return ''

        query = {}
        for param in self.params.split(','):
            key, val = param.split('=')
            query[key] = val

        return '?' + urlencode(query)


@register.tag()
def ekubo(parser, token):
    tag_name, path, params = token.split_contents()

    return EkuboNode(path, params[1:-1])


def _get_path(value):
    if isinstance(value, (str, unicode)):
        path = value
    else:
        # if ImageField
        path = value.name

    return path
