__author__ = 'kako'


class BadRequestError(Exception):
    status_code = 400


class NotAuthenticatedError(Exception):
    status_code = 401


class NotAuthorizedError(Exception):
    status_code = 403


class NotFoundError(Exception):
    status_code = 404


class MethodNotAllowedError(Exception):
    status_code = 405


class InvalidOperationError(Exception):
    pass
