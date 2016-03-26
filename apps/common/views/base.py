__author__ = 'kako'

import logging
import re

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.views.generic import View

from ..exceptions import NotAuthenticatedError, NotAuthorizedError


logger = logging.getLogger('django')


def handle_exception(func):
    # Non debug, catch and process exception
    def wrapper_func(*args, **kwargs):
        try:
            res = func(*args, **kwargs)

        except Exception as e:
            if settings.DEBUG and not hasattr(e, 'status_code'):
                raise
            view, request = args[0:2]
            return view.process_exception(request, e)

        else:
            return res
    return wrapper_func


class SafeView(View):
    """
    Base class for views that use authorization checks and generic
    error handling.
    """
    error_template = 'apps/error.html'
    require_login = True
    permissions = {}

    @classmethod
    def authorize(cls, request, action):
        """
        Default authorization mechanism.
        """
        if not cls.require_login or request.user.is_superuser:
            # Login not required, or superuser, allow fine
            return

        elif not request.user.is_authenticated():
            # User not authenticated, error
            raise NotAuthenticatedError("User must be authenticated to "
                                        "access this resource.")

        # OK, check permissions
        action_perms = cls.permissions.get(action)
        if (action_perms and
                not request.user.get_all_permissions().intersection(action_perms)):
            # Permissions required not given to user
            raise NotAuthorizedError("User not authorized to {} this "
                                     "resource.".format(action))

    @classmethod
    def process_exception(cls, request, exception):
        """
        Process the given exception, by logging it with the adequate log level
        and rendering to the user.
        """
        # Determine status code (500 is terrible)
        status_code = getattr(exception, 'status_code', 500)

        # Log the exception
        if status_code == 500:
            logger.exception(exception)
        else:
            logger.debug(exception)

        # Build context for error template
        context = {'error': exception.__class__.__name__.replace('Error', ''),
                   'status': status_code,
                   'message': str(exception)}

        # Render it
        return render(request, cls.error_template,
                      context, status=status_code)

    @handle_exception
    def dispatch(self, request, *args, **kwargs):
        """
        Wrapper for all requests, authorize and execute the requested method.
        """
        self.authorize(request, kwargs.get('action', 'view'))
        return super(SafeView, self).dispatch(request, *args, **kwargs)


class ReadOnlyResourceView(SafeView):
    """
    Base class for views that provide read-only operations for a model's
    collection (list) and instance (detail).

    In most cases, you won't need to modify any methods, only assign the model
    and the templates.
    """
    model = None
    list_template = None
    detail_template = None
    search_form = None

    # Helper class methods

    @classmethod
    def build_filters(cls, qd, **kwargs):
        """
        Build the filters dict from a querydict (parsed querystring).

        Override if you need to do add something based on passed kwargs, but
        DO NOT MODIFY the passed querydict.
        """
        # Start with fresh dict
        filters = {}

        # Populate it
        for k in qd:
            # Get value depending on key
            if k in ('page', 'page_size',):
                # page or page_size, skip it (not handled by filter)
                continue
            elif k.endswith('__in') or k.endswith('__range'):
                # membership, get value as list
                v = qd.getlist(k)
            else:
                # others, get value a simple object
                v = qd.get(k)

            # Add key:value to filter if it has a value
            if v:
                filters[k] = v

        # Return the resulting filters dict
        return filters

    @classmethod
    def filter_objects(cls, user, qd, **kwargs):
        """
        Filter the model queryset for the given user and querydict.

        Override if you need to do so further filtering outside of the standard
        filter construction.
        """
        # Build filters from querydict
        filters = cls.build_filters(qd, **kwargs)

        # Get the filtered queryset and return it
        qs = cls.model.objects.filter(**filters).for_user(user)
        return qs

    @classmethod
    def get_instance_context(cls, request, obj):
        """
        Build the context for the single instance view.

        Override if you need something different from the default, which is:
          - model verbose name singular: instance
        """
        return {cls.model._meta.verbose_name.replace(' ', ''): obj}

    @classmethod
    def get_list_context(cls, request, objs):
        """
        Build the context for the list view.

        Override if you need something different from the default, which is:
          - model verbose name plural: queryset
          - qs: querystring
        """
        return {cls.model._meta.verbose_name_plural.replace(' ', ''): objs,
                'qs': re.sub(r'[&]?page=\d+', '', request.GET.urlencode())}

    @classmethod
    def get_object(cls, user, pk):
        """
        Get a single object for the given primary key.

        Override only if you need to do something really odd.
        """
        return cls.model.objects.filter(id=pk).for_user(user).get()

    # Main http methods (proxy to worker methods)

    def get(self, request, pk=None, action=None, **kwargs):
        """
        Handler for HTTP GET request.

        Overriding this method is not recommended, override the method specific
        to the custom behaviour instead.
        """
        if pk:
            return self.show_instance(request, pk)
        else:
            return self.show_list(request, **kwargs)

    # Worker methods

    def show_list(self, request, status=200, **kwargs):
        """
        Render the list view.

        Overriding this method is not recommended, override the method specific
        to the custom behaviour instead.
        """
        # First get the filtered objects
        objs = self.filter_objects(request.user, request.GET, **kwargs)

        # Now get the paginated subset of objects
        page_size = request.GET.get('page_size') or 20
        page_num = request.GET.get('page', 1)
        p = Paginator(objs, page_size)
        try:
            objs = p.page(page_num)
        except PageNotAnInteger:
            objs = p.page(1)
        except EmptyPage:
            objs = p.page(p.num_pages)

        # Build the context (include form if required)
        context = self.get_list_context(request, objs)
        if self.search_form:
            search_form = self.search_form(request.GET, user=request.user)
            context['search_form'] = search_form

        # Finally, render the template
        return render(request, self.list_template, context, status=status)

    def show_instance(self, request, pk):
        """
        Render the single-object view.

        Overriding this method is not recommended, override the method specific
        to the custom behaviour instead.
        """
        # Get single object
        obj = self.get_object(request.user, pk)

        # Build context
        context = self.get_instance_context(request, obj)
        return render(request, self.detail_template, context)


class StandardResourceView(ReadOnlyResourceView):
    """
    Base class for resource views that provide the full set of CRUD operations
    for a model's collection (list) and instance (detail).

    In most cases, you won't need to modify any methods, only assign the model,
    the templates, the edit form and the permissions.
    """
    edit_template = None
    main_form = None
    sub_form = None
    collection_view_name = None

    # Main http methods (proxy to worker methods)
    # Usually you won't need to override, unless you're doing something weird

    def get(self, request, pk=None, action=None, **kwargs):
        """
        Handler for HTTP GET method.

        Overriding this method is not recommended, override the method specific
        to the custom behaviour instead.
        """
        # User wants to add or edit, show edit forms
        if action in ('add', 'edit'):
            return self.show_forms(request, pk)

        # Other cases, handle are super class
        return super(StandardResourceView, self).get(request, pk,
                                                     action, **kwargs)

    def post(self, request, pk=None, action=None, **kwargs):
        """
        Handler for HTTP POST method.

        Overriding this method is not recommended, override the method specific
        to the custom behaviour instead.
        """
        return self.upsert_instance(request, pk, **kwargs)

    def put(self, request, pk, action=None, **kwargs):
        """
        Handler for HTTP PUT method.

        Overriding this method is not recommended, override the method specific
        to the custom behaviour instead.
        """
        return self.upsert_instance(request, pk, **kwargs)

    def delete(self, request, pk, action=None, **kwargs):
        """
        Handler for HTTP DELETE method.

        Overriding this method is not recommended, override the method specific
        to the custom behaviour instead.
        """
        return self.delete_instance(request, pk, **kwargs)

    # Worker methods
    # Override to modify standard behaviour

    def show_forms(self, request, pk):
        """
        Render the main form and subform for the given instance pk.

        Override this method if you need to customize the context.
        """
        # Fetch object (or use None for new one)
        obj = pk and self.get_object(request.user, pk) or None

        # Initialize the main form and build context
        main_form = self.main_form(instance=obj, user=request.user,
                                   prefix='main')
        context = {self.model._meta.verbose_name.replace(' ', ''): obj,
                   'main_form': main_form}

        # Add subform to context if required
        if pk and self.sub_form:
            context['sub_form'] = self.sub_form(instance=obj,
                                                user=request.user, prefix='sub')

        # Render view
        return render(request, self.edit_template, context)

    def upsert_instance(self, request, pk, **kwargs):
        """
        Save the main form (and subform is the instance is not new) and redirect
        to the collection view.

        Override this method if you need to customize the processing of forms.
        """
        # Fetch the object (or use None for new one)
        obj = pk and self.get_object(request.user, pk) or None

        # Process the main form and build context
        main_form = self.main_form(request.POST, instance=obj,
                                   user=request.user, prefix='main')
        context = {self.model._meta.verbose_name.replace(' ', ''): obj,
                   'main_form': main_form}

        # Process subform if required and add to context
        if pk and self.sub_form:
            sub_form = self.sub_form(request.POST, instance=obj,
                                     user=request.user, prefix='sub')
            context['sub_form'] = sub_form
        else:
            sub_form = None

        # Valiate forms
        if main_form.is_valid() and (not sub_form or sub_form.is_valid()):
            # Everything's valid, save the form
            main_form.save()
            if sub_form:
                sub_form.save()

            # Now redirect to collection view, passing kwargs (subresources work too)
            view_name = (self.collection_view_name or
                         self.model._meta.verbose_name_plural.lower().replace(' ', ''))
            return redirect(view_name, **kwargs)

        else:
            # Invalid, render forms again with errors
            return render(request, self.edit_template, context, status=400)

    def delete_instance(self, request, pk, **kwargs):
        """
        Delete the instance matching the given pk and redirect to collection view.

        Override if you need to run checks or delete other objects before or
        after deleting the instance.
        """
        obj = self.get_object(request.user, pk)
        obj.delete()

        # Now redirect to collection view, passing kwargs (subresources work too)
        view_name = (self.collection_view_name or
                     self.model._meta.verbose_name_plural.lower().replace(' ', ''))
        return redirect(view_name, **kwargs)
