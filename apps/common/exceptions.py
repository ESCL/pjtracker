__author__ = 'kako'


class ClientError(Exception):
    status_code = 400


class AuthenticationError(Exception):
    status_code = 401


class AuthorizationError(Exception):
    status_code = 403
