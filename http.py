# coding: utf-8

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils import simplejson as json


class JSONResponse(HttpResponse):

    def __init__(self, data={}, cls=DjangoJSONEncoder, status=200, content_type='application/json'):
        super(JSONResponse, self).__init__(json.dumps(data, cls=cls),
                content_type=content_type)

