__author__ = 'kako'

from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import View
from django.template.defaultfilters import slugify


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


class ReadOnlyResourceView(View):
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

    # Main http methods (proxy to worker methods)

    @handle_exception
    def get(self, request, pk=None, action=None, **kwargs):
        if pk:
            return self.show_instance(request, pk)
        else:
            return self.show_list(request, **kwargs)

    # Worker methods

    def show_list(self, request, status=200, **kwargs):
        context = {self.model._meta.verbose_name_plural.replace(' ', ''): self.filter_objects(request.user, request.GET, **kwargs)}
        return render(request, self.list_template, context, status=status)

    def show_instance(self, request, pk):
        context = {self.model._meta.verbose_name.replace(' ', ''): self.get_object(request.user, pk)}
        return render(request, self.detail_template, context)


class StandardResourceView(ReadOnlyResourceView):
    """
    Standard resource view that provides CRUD operations for a model's
    collection (list) and instance (detail).

    In most cases, you won't need to modify any methods, only assign the model,
    the templates and the edit form.
    """
    edit_template = None
    main_form = None
    sub_form = None
    collection_view_name = None

    # Main http methods (proxy to worker methods)
    # Usually you won't need to override, unless you're doing something weird

    @handle_exception
    def get(self, request, pk=None, action=None, **kwargs):
        if action in ('add', 'edit'):
            return self.show_forms(request, pk)

        return super(StandardResourceView, self).get(request, pk, action, **kwargs)

    @handle_exception
    def post(self, request, pk=None, **kwargs):
        if pk:
            return self.put(request, pk)
        return self.upsert_instance(request, pk)

    @handle_exception
    def put(self, request, pk, **kwargs):
        return self.upsert_instance(request, pk)

    @handle_exception
    def delete(self, request, pk, **kwargs):
        return self.delete_instance(request, pk)

    # Worker methods
    # Override to modify standard behaviour

    def show_forms(self, request, pk):
        obj = pk and self.get_object(request.user, pk) or None
        main_form = self.main_form(instance=obj, prefix='main')
        context = {self.model._meta.verbose_name.replace(' ', ''): obj, 'main_form': main_form}
        if self.sub_form:
            context['sub_form'] = self.sub_form(instance=obj, prefix='sub')
        return render(request, self.edit_template, context)

    def upsert_instance(self, request, pk):
        obj = pk and self.get_object(request.user, pk) or None
        main_form = self.main_form(request.POST, instance=obj, user=request.user, prefix='main')
        context = {self.model._meta.verbose_name.replace(' ', ''): obj, 'main_form': main_form}

        if self.sub_form:
            sub_form = self.sub_form(request.POST, instance=obj, user=request.user, prefix='sub')
            context['sub_form'] = sub_form
        else:
            sub_form = None

        if main_form.is_valid() and (not sub_form or sub_form.is_valid()):
            main_form.save()
            if sub_form:
                sub_form.save()
            return redirect(self.collection_view_name or slugify(self.model._meta.verbose_name_plural))

        else:
            return render(request, self.edit_template, context, status=400)

    def delete_instance(self, request, pk):
        obj = self.get_object(request.user, pk)
        obj.delete()
        return self.show_list(request, status=204)
