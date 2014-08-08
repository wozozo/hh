# coding: utf-8

import json

from django import http
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View as _View
from django.views.generic.edit import TemplateResponseMixin
from django.views.generic.detail import BaseDetailView, SingleObjectMixin

from decorators import login_required_json
from http import DjangoJSONEncoder


class View(_View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(View, self).dispatch(*args, **kwargs)


# class LoginRequiredView(View):
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(LoginRequiredView, self).dispatch(*args, **kwargs)


class JSONResponseMixin(object):
    """
    ref. https://docs.djangoproject.com/en/1.3/topics/class-based-views/#more-than-just-html
    """
    def render_success(self, context=None):
        success = {'code': 'SUCCESS'}
        if context:
            success.update(context)
        return self.render_to_response(success)

    def render_fail(self, context, data=None):
        if data:
            context.update(data)
        return self.render_to_response(context)

    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context, cls=DjangoJSONEncoder)


class JSONView(JSONResponseMixin, SingleObjectMixin, View):
    pass


class JSONDetailView(JSONResponseMixin, BaseDetailView):
    post_slug = None

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        if self.post_slug:
            slug_field = self.post_slug
            slug = self.request.POST.get(slug_field)
            queryset = queryset.filter(**{slug_field: slug})

        try:
            return queryset.get()
        except ObjectDoesNotExist:
            pass
        super(JSONDetailView, self).get_object(queryset)


class PlayerTemplateResponseMixin(TemplateResponseMixin):

    def render_to_response(self, context, **response_kwargs):
        if 'cast' in context and context['cast'] == self.request.user:
            context['player'] = True
        else:
            context['player'] = False

        return super(PlayerTemplateResponseMixin, self).render_to_response(context, **response_kwargs)


class AssignUserView(object):

    def get_initial(self):
        initial = super(AssignUserView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['user'] = self.request.user


class LoginRequiredJSONMixin(object):
    """
    View mixin which verifies that the user has authenticated.

    NOTE:
        This should be the left-most mixin of a view.

    NOTE:
        Based on django-braces.views.LoginRequiredMixin

    """

    @method_decorator(login_required_json)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredJSONMixin, self).dispatch(*args, **kwargs)

