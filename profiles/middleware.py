import datetime
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class ActiveUserMiddleware(MiddlewareMixin):
    """This snippet allows to see the last time a user was seen."""

    def process_request(self, request):
        """Process the request."""
        current_user = request.user
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            # save the last time the user was seen in the cache
            cache.set('seen_%s' % (current_user.username),
                      now, settings.USER_LAST_SEEN_TIMEOUT)
