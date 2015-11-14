__author__ = 'kako'

from django.shortcuts import render, redirect
from django.views.generic import View

from ...notifications.models import Notification


class HomeView(View):
    template_name = 'apps/home.html'

    def get(self, request):
        if not request.user.is_authenticated():
            return redirect('public', page='home')

        notifs = Notification.objects.for_user(request.user)
        notifs = notifs.filter(status=Notification.STATUS_ENABLED)
        context = {'user': request.user,
                   'notifications': notifs}
        return render(request, self.template_name, context)

