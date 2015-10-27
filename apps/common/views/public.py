__author__ = 'kako'

from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    template_name = 'public/home.html'

    def get(self, request):
        context = {'user': request.user}
        return render(request, self.template_name, context)
