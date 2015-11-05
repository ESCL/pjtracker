__author__ = 'kako'

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

from ...notifications.models import Notification


class HomeView(View):
    template_name = 'apps/home.html'

    @method_decorator(login_required)
    def get(self, request):
        context = {'user': request.user,
                   'notifications': Notification.objects.for_user(request.user)}
        return render(request, self.template_name, context)

