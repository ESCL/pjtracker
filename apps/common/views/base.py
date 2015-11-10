__author__ = 'kako'

from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import View

from ..exceptions import AuthorizationError


def handle_exception(func):
    if settings.DEBUG:
        # For debug, don't handle so devs get stacktrace
        return func

    # Non debug, catch and process exception
    def wrapper_func(*args, **kwargs):
        try:
            res = func(*args, **kwargs)

        except Exception as e:
            view, request = args[0:2]
            return view.process_exception(request, e)

        else:
            return res
    return wrapper_func


class SafeView(View):
    error_template = None

    @classmethod
    def process_exception(cls, request, exception):
        # Build the context from the error data
        status_code = getattr(exception, 'status_code', 500)
        context = {'error': exception.__class__.__name__,
                   'status': status_code,
                   'message': str(exception)}

        # Render the error template with the data
        return render(request, cls.error_template,
                      context, status=status_code)

    @handle_exception
    def dispatch(self, request, *args, **kwargs):
        return super(SafeView, self).dispatch(request, *args, **kwargs)


class ReadOnlyResourceView(SafeView):
    """
    Standard resource view that provides read-only operations for a model's
    collection (list) and instance (detail).

    In most cases, you won't need to modify any methods, only assign the model
    and the templates.
    """
    model = None
    list_template = None
    detail_template = None
    error_template = 'apps/error.html'

    # Helper class methods

    @classmethod
    def build_filters(cls, qs, *args, **kwargs):
        return {k: qs.get(k) for k in qs.keys()}

    @classmethod
    def filter_objects(cls, user, qs, **kwargs):
        filters = cls.build_filters(qs, **kwargs)
        return cls.model.objects.filter(**filters).for_user(user)

    @classmethod
    def get_object(cls, user, pk):
        return cls.model.objects.filter(id=pk).for_user(user).get()

    # Main http methods (proxy to worker methods)

    def get(self, request, pk=None, action=None, **kwargs):
        if pk:
            return self.show_instance(request, pk, **kwargs)
        else:
            return self.show_list(request, **kwargs)

    # Worker methods

    def show_list(self, request, status=200, **kwargs):
        objs = self.filter_objects(request.user, request.GET, **kwargs)
        context = {self.model._meta.verbose_name_plural.replace(' ', ''): objs}
        return render(request, self.list_template, context, status=status)

    def show_instance(self, request, pk, **kwargs):
        obj = self.get_object(request.user, pk)
        context = {self.model._meta.verbose_name.replace(' ', ''): obj}
        return render(request, self.detail_template, context)


class StandardResourceView(ReadOnlyResourceView):
    """
    Standard resource view that provides CRUD operations for a model's
    collection (list) and instance (detail).

    In most cases, you won't need to modify any methods, only assign the model,
    the templates, the edit form and the permissions.
    """
    edit_template = None
    main_form = None
    sub_form = None
    collection_view_name = None

    # Allowed permission per action
    permissions = {
        'add': ('add',),
        'edit': ('change',),
    }

    # Authorization methods for edit views

    @classmethod
    def authorize(cls, request, action):
        """
        Authorize the user by checking that he has access to the given action
        for the view model. It also allows partial access (to specific fields
        in the model).
        """
        if not action or request.user.is_superuser:
            # No need to check permissions, OK
            return
        else:
            # Check if user is allowed to execute the action
            for a in request.user.get_allowed_actions_for(cls.model):
                if a[0] in cls.permissions[action]:
                    return

        # If we got th  is far user is not authorized, raise error
        raise AuthorizationError(
            'User {} is not allowed to {} {}.'.format(request.user, action,
                                                      cls.model._meta.verbose_name_plural)
        )

    @handle_exception
    def dispatch(self, request, *args, action=None, **kwargs):
        self.authorize(request, action)
        return super(SafeView, self).dispatch(request, *args, action=action, **kwargs)

    # Main http methods (proxy to worker methods)
    # Usually you won't need to override, unless you're doing something weird

    def get(self, request, pk=None, action=None, **kwargs):
        if action in ('add', 'edit'):
            return self.show_forms(request, pk)

        return super(StandardResourceView, self).get(request, pk, action, **kwargs)

    def post(self, request, pk=None, action=None, **kwargs):
        if pk:
            return self.put(request, pk, **kwargs)
        return self.upsert_instance(request, pk, **kwargs)

    def put(self, request, pk, action=None, **kwargs):
        return self.upsert_instance(request, pk, **kwargs)

    def delete(self, request, pk, action=None, **kwargs):
        return self.delete_instance(request, pk, **kwargs)

    # Worker methods
    # Override to modify standard behaviour

    def show_forms(self, request, pk):
        """
        Render the main form and subform for the given instance pk.
        """
        obj = pk and self.get_object(request.user, pk) or None
        main_form = self.main_form(instance=obj, user=request.user, prefix='main')
        context = {self.model._meta.verbose_name.replace(' ', ''): obj, 'main_form': main_form}

        if pk and self.sub_form:
            # Existing instance and sub_form defined, use it
            context['sub_form'] = self.sub_form(instance=obj, user=request.user, prefix='sub')

        return render(request, self.edit_template, context)

    def upsert_instance(self, request, pk, **kwargs):
        """
        Save the main form (and subform is the instance is not new) and redirect
        to the collection view.
        """
        obj = pk and self.get_object(request.user, pk) or None
        main_form = self.main_form(request.POST, instance=obj, user=request.user, prefix='main')
        context = {self.model._meta.verbose_name.replace(' ', ''): obj, 'main_form': main_form}

        if pk and self.sub_form:
            # Existing instance and sub_form defined, use it
            sub_form = self.sub_form(request.POST, instance=obj, user=request.user, prefix='sub')
            context['sub_form'] = sub_form
        else:
            sub_form = None

        if main_form.is_valid() and (not sub_form or sub_form.is_valid()):
            # If all defined forms are valid, save them
            main_form.save()
            if sub_form:
                sub_form.save()

            # Now redirect to collection view, passing kwargs (subresources work too)
            view_name = self.collection_view_name or self.model._meta.verbose_name_plural.lower().replace(' ', '')
            return redirect(view_name, **kwargs)

        else:
            # Invalid, render forms again with errors
            return render(request, self.edit_template, context, status=400)

    def delete_instance(self, request, pk, **kwargs):
        """
        Delete the instance matching the given pk and redirect to collection view.
        """
        obj = self.get_object(request.user, pk)
        obj.delete()

        # Now redirect to collection view, passing kwargs (subresources work too)
        view_name = self.collection_view_name or self.model._meta.verbose_name_plural.lower().replace(' ', '')
        return redirect(view_name, **kwargs)
