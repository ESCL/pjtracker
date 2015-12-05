__author__ = 'kako'

from django.http import HttpResponseRedirect
from oauth2_provider.views.base import AuthorizationView, TokenView, RevokeTokenView
from oauth2_provider.exceptions import OAuthToolkitError
from oauth2_provider.http import HttpResponseUriRedirect


class CustomAuthorizationView(AuthorizationView):
    # TODO: Change the form template, it sucks

    def form_valid(self, form):
        try:
            # Get credentials
            credentials = {
                'client_id': form.cleaned_data.get('client_id'),
                'redirect_uri': form.cleaned_data.get('redirect_uri'),
                'response_type': form.cleaned_data.get('response_type', None),
                'state': form.cleaned_data.get('state', None),
            }

            # Get other data and build uri
            scopes = form.cleaned_data.get('scope')
            allow = form.cleaned_data.get('allow')
            uri, headers, body, status = self.create_authorization_response(
                request=self.request, scopes=scopes,
                credentials=credentials, allow=allow
            )

            # Check if use has domain, send that param as well
            if self.request.user.domain:
                uri += '&account={}'.format(self.request.user.owner.id)

            # Set success url and redirect
            self.success_url = uri
            return HttpResponseUriRedirect(self.success_url)

        except OAuthToolkitError as error:
            return self.error_response(error)
