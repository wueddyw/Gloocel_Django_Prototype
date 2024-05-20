from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions

"""
Currently using hours for testing. You may want to change 
to minutes when pushing to production
"""
EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 2)
# EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 15)

"""
Checks the user's token to see if it expiring or not
"""
class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            model = self.get_model()
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive or deleted')

        if token.created < timezone.now() - timedelta(hours=EXPIRE_HOURS):
        # if token.created < timezone.now() - timedelta(minutes=EXPIRE_MINUTES):
            raise exceptions.AuthenticationFailed('Token has expired')

        return (token.user, token)