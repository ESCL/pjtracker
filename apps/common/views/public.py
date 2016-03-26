__author__ = 'kako'

from django.shortcuts import render
from django.template import TemplateDoesNotExist
from .base import SafeView
from ..exceptions import NotFoundError


class PublicView(SafeView):
    template_base = 'public/{}.html'
    require_login = False

    def get(self, request, page):
        """
        HTTP GET handler, attempts to render the template for the given page
        and raises a 404 if it's not found.
        """
        try:
            return render(request, self.template_base.format(page), {})
        except TemplateDoesNotExist:
            raise NotFoundError("The requested resources does not exist.")
