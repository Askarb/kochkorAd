from django.conf import settings


class WebappMiddleware(object):

    def __init__(self, response):
        self.response = response

    def __call__(self, request, *args, **kwargs):
        request.debug = settings.DEBUG
        return self.response(request)
