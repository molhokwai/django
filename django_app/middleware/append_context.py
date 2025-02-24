from django.conf import settings
from django.utils.translation import gettext_lazy as _


class AppendContextMiddleware:
    """
        src: https://stackoverflow.com/questions/51625342/django-how-to-modify-template-context-from-middleware
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ------------
        # LIVE, LOCAL, PLATFORM...
        # ------------
        request.IS_LIVE = settings.IS_LIVE
        request.IS_LOCAL = settings.IS_LOCAL
        request.IS_LOCAL = settings.IS_LOCAL
        request.IS_PYANY = settings.IS_PYANY

        response = self.get_response(request)
        return response
