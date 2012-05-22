# coding: utf-8

from django.conf import settings
from django.utils.importlib import import_module


class ModelBackend(object):
    """
    Authenticates against django.contrib.auth.models.User.
    """

    def __init__(self):
        path = settings.USER_CLASS_PATH
        i = path.rfind('.')
        module, attr = path[:i], path[i+1:]

        self.USER_CLASS = getattr(import_module('core.models'), attr)

    # TODO: Model, login attribute name and password attribute name should be
    # configurable.
    def authenticate(self, username=None, password=None):

        try:
            user = self.USER_CLASS.objects.get(username=username)
            if user.check_password(password):
                return user
        except self.USER_CLASS.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.USER_CLASS.objects.get(pk=user_id)
        except self.USER_CLASS.DoesNotExist:
            return None


# class TwitterOAuthBackend(object):
#     raise NotImplementedError


# class FacebookOAuthBackend(object):
#     raise NotImplementedError
