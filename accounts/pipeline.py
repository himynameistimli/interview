import logging

from social_core.backends.google import GoogleOAuth2

logger = logging.getLogger(__name__)


def register_user(strategy, user, details, is_new, *args, **kwargs):
    backend = kwargs['backend']
    if isinstance(backend, GoogleOAuth2):
        if is_new:
            user.is_email_verified = True
            user.save()
    else:
        raise NotImplemented()

