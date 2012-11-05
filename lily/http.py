# coding: utf-8

import json

from django.core.serializers.json import DjangoJSONEncoder as _DjangoJSONEncoder
from django.http import HttpResponse


class DjangoJSONEncoder(_DjangoJSONEncoder):

    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, o):
        return super(DjangoJSONEncoder, self).default(o)


class JSONResponse(HttpResponse):

    def __init__(self, data={}, cls=DjangoJSONEncoder, status=200, content_type='application/json'):
        super(JSONResponse, self).__init__(json.dumps(data, cls=cls),
                content_type=content_type)

