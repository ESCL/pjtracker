__author__ = 'kako'

from django.shortcuts import render
from django.views.generic import View

from ...notifications.models import Notification


class HomeView(View):
    template_name = 'apps/home.html'

    def get(self, request):
        context = {'user': request.user,
                   'notifications': Notification.objects.for_user(request.user)}
        return render(request, self.template_name, context)

