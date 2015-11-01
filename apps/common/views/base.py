__author__ = 'kako'

from django.shortcuts import render
from django.views.generic import View


def handle_exception(func):
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
    def build_filters(cls, qs):
        return qs

    @classmethod
    def filter_objects(cls, user, qs):
        filters = cls.build_filters(qs)
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
            return self.show_list(request)

    # Worker methods

    def show_list(self, request, status=200):
        context = {self.model._meta.verbose_name_plural.replace(' ', ''): self.filter_objects(request.user, request.GET)}
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
    edit_form = None

    # Main http methods (proxy to worker methods)
    # Usually you won't need to override, unless you're doing something weird

    @handle_exception
    def get(self, request, pk=None, action=None, **kwargs):
        if action == 'edit':
            return self.show_form(request, pk)

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
    def delete(self, request, pk):
        return self.delete_instance(request, pk)

    # Worker methods
    # Override to modify standard behaviour

    def show_form(self, request, pk):
        obj = pk and self.get_object(request.user, pk) or None
        form = self.edit_form(instance=obj)
        context = {self.model._meta.verbose_name.replace(' ', ''): obj, 'form': form}
        return render(request, self.edit_template, context)

    def upsert_instance(self, request, pk):
        obj = pk and self.get_object(request.user, pk) or None
        form = self.edit_form(instance=obj)
        if form.is_valid():
            form.save()
            return self.show_list(request, status=201)
        else:
            context = {self.model._meta.verbose_name.replace(' ', ''): obj, 'form': form}
            return render(request, self.edit_template, context, status=400)

    def delete_instance(self, request, pk):
        obj = self.get_object(request.user, pk)
        obj.delete()
        return self.show_list(request, status=204)
