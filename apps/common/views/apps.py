__author__ = 'kako'

from django.shortcuts import render, redirect
from django.views.generic import View

from ...notifications.models import Notification


class HomeView(View):
    template_name = 'apps/home.html'

    def get(self, request):
        """
        HTTP GET handler, displays notifications for user or redirects to
        public home if user is not authenticated.
        """
        # Check if authenticated, if not redirect to public home
        if not request.user.is_authenticated():
            return redirect('public', page='home')

        # Build context with notifications for user
        notifs = Notification.objects.for_user(request.user).enabled()
        context = {'user': request.user,
                   'notifications': notifs}

        # Render template with context
        return render(request, self.template_name, context)

