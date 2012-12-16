# coding: utf-8

# from urllib import urlencode
# from urlparse import parse_qsl

from django import template

register = template.Library()


@register.filter
def resize(value, params):

    if isinstance(value, str):
        path = value
    else:
        # ImageField の場合
        path = value.name

    return '{}?{}'.format(path, params)
