__author__ = 'kako'

from django.shortcuts import render, redirect
from django.template import TemplateDoesNotExist
from django.http import Http404
from .base import SafeView, handle_exception


class PublicView(SafeView):
    template_base = 'public/{}.html'

    @handle_exception
    def get(self, request, page):
        try:
            return render(request, self.template_base.format(page), {})
        except TemplateDoesNotExist:
            raise Http404()
