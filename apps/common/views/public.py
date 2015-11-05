__author__ = 'kako'

from django.shortcuts import render, redirect
from django.views.generic import View


class HomeView(View):
    template_name = 'public/home.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('home-app')

        return render(request, self.template_name, {})

