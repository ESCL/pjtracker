__author__ = 'kako'

import logging

from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from oauth2_provider.models import AccessToken
from tastypie.authentication import Authentication


class OAuthError(RuntimeError):
    """
    Generic exception for OAuth.
    """
    def __init__(self, message='OAuth error occurred.'):
        self.message = message


class OAuth2Authentication(Authentication):
    """
    OAuth authenticator.

    This Authentication method checks for a provided HTTP_AUTHORIZATION
    and looks up to see if this is a valid OAuth Access Token
    """
    def __init__(self, realm='API', *args, **kwargs):
        super(OAuth2Authentication, self).__init__(*args, **kwargs)
        self.realm = realm

    @staticmethod
    def _get_key(request):
        """
        Get the api key from the request.

        :param request: http request
        :return: key value
        """
        # Get key from querystring
        key = request.GET.get('oauth_consumer_key')

        if not key:
            # Not there, get from POST body
            key = request.POST.get('oauth_consumer_key')

        if not key:
            # Not there, get from META headers
            auth_header_value = request.META.get('HTTP_AUTHORIZATION')
            if auth_header_value:
                key = auth_header_value.split(' ')[1]

        # Return whatever you got
        return key

    @staticmethod
    def _verify_access_token(key):
        """
        Verify that the access token exists and has not expired

        :param key: key of the token
        :return: token if valid
        """
        try:
            # Check if key is in AccessToken key
            token = AccessToken.objects.get(token=key)

            # Check if token has expired, raise exception if so
            if token.expires < timezone.now():
                raise OAuthError('AccessToken has expired.')

        except AccessToken.DoesNotExist:
            # Access token not found, error
            raise OAuthError("AccessToken not found.")

        # OK, return token
        return token

    def is_authenticated(self, request, **kwargs):
        """
        Verify 2-legged oauth request. Parameters accepted as
        values in "Authorization" header, or as a GET request
        or in a POST body.
        """
        try:
            # Get key and raise error if none found
            key = self._get_key(request)
            if not key:
                raise Exception('No consumer_key found.')

            # Verify token (which might raise an error)
            token = self._verify_access_token(key)

        except KeyError as e:
            # Key error, set user to Anon and return False
            logging.exception("OAuth 2.0 auth error: {}".format(e))
            request.user = AnonymousUser()
            return False

        except Exception as e:
            # Another error, return False
            logging.exception("OAuth 2.0 auth error: {}".format(e))
            return False

        else:
            # Successful, set the request user to the token user and
            # oauth_consumer_key on request in case we need later
            request.user = token.user
            request.META['oauth_consumer_key'] = key
            return True
