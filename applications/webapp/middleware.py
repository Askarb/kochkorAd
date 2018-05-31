from project import settings

from applications.webapp.models import Variable


class WebappMiddleware(object):

    def __init__(self, response):
        self.response = response

    def __call__(self, request, *args, **kwargs):
        request.debug = settings.DEBUG
        request.site_url = settings.SITE_URL
        request.fb_app_id = settings.SOCIAL_AUTH_FACEBOOK_KEY
        request.email = Variable.objects.get(name='email').value
        request.whatsapp = settings.WHATSAPP_NUMBER
        return self.response(request)
