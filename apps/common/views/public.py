__author__ = 'kako'

from django.shortcuts import render, redirect
from django.views.generic import View


class PublicView(View):
    template_base = 'public/{}.html'

    def get(self, request, page):
        if request.user.is_authenticated():
            return redirect('home-app')

        return render(request, self.template_base.format(page), {})
