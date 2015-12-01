__author__ = 'kako'

from django.conf import settings


def domain(request):
    """
    Returns context variables related to the domain and company.
    """
    return {
        'COMPANY': getattr(settings, 'COMPANY_INFO', {}),
        'APP': getattr(settings, 'APP_INFO', {})
    }
