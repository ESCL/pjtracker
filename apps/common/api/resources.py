__author__ = 'kako'

from tastypie import resources, exceptions, http

from ..exceptions import NotAuthenticatedError


class OwnedResource(resources.ModelResource):
    """
    Base model resource for owned entity models, which attempts to
    filter the queryset using for_user and returns a 401 if that fails (see
    the implementation of for_user to know why that's OK).
    """
    def apply_filters(self, request, applicable_filters):
        qs = super(OwnedResource, self).apply_filters(request, applicable_filters)
        try:
            qs = qs.for_user(request.user)
        except NotAuthenticatedError as e:
            raise exceptions.ImmediateHttpResponse(http.HttpUnauthorized(e))
        return qs
