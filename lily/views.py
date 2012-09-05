# coding: utf-8

from django import http
from django.utils import simplejson as json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View as _View
from django.views.generic.edit import TemplateResponseMixin
from django.views.generic.detail import BaseDetailView, SingleObjectMixin
from django.views.generic.list import BaseListView

# from lily.decorators import login_required


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
    def success(self, context=None):
        success = {'code': 'SUCCESS'}
        if context:
            success.update(context)
        return self.render_to_response(success)

    def fail(self, context, data=None):
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
        return json.dumps(context)


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
