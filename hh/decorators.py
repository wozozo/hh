# coding: utf-8

from functools import wraps

from http import JSONResponse

def login_required_json(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JSONResponse({'code': 'NOT_LOGIN'})
        response = func(request, *args, **kwargs)
        return response
    return wrapper
