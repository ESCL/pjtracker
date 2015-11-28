__author__ = 'kako'

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
from ..common.forms import OwnedEntityForm, ModernForm


class UserForm(OwnedEntityForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'groups', )


class AdminUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'owner',)


class UserSearchForm(ModernForm):
    username__icontains = forms.CharField(max_length=32, label='Username')
    first_name__icontains = forms.CharField(max_length=32, label='First name')
    last_name__icontains = forms.CharField(max_length=32, label='Last name')