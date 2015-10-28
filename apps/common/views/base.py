__author__ = 'kako'

from django.shortcuts import render
from django.views.generic import View


def handle_exception(func):
    def wrapper_func(*args, **kwargs):
        try:
            res = func(*args, **kwargs)

        except Exception as e:
            view = args[0]
            h_args = args[1:] + (e,)
            return view.process_exception(*h_args)

        else:
            return res
    return wrapper_func


class StandardResourceView(View):
    list_template = None
    detail_template = None
    edit_template = None
    error_template = 'apps/error.html'
    edit_form = None
    model = None

    @classmethod
    def build_filters(cls, qs):
        return qs

    @classmethod
    def filter_objects(cls, user, qs):
        filters = cls.build_filters(qs)
        return cls.model.objects.filter(**filters).for_user(user)

    @classmethod
    def get_object(cls, user, id):
        return cls.model.objects.filter(id=id).for_user(user).get()

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
    def get(self, request, pk=None, action=None):
        if pk:
            print('single object')
            # Get object and build context
            obj = self.get_object(request.user, pk)

            # Determine template and add form if required
            if action == 'edit':
                print('edit')
                template = self.edit_template
                context = {'form': self.edit_form(instance=obj)}
            else:
                context = {'object': obj}
                template = self.detail_template

        else:
            print('list')
            # Template is alwatys the same
            template = self.list_template

            # Determine context based on action
            if action == 'edit':
                print('edit')
                context= {'form': self.edit_form()}
            else:
                context = {'objects': self.filter_objects(request.user, request.GET)}

        return render(request, template, context, status=200)

    @handle_exception
    def post(self, request):
        form = self.edit_form(request.POST)

        if form.is_valid():
            form.save()
            template = self.list_template
            context = {'objects': self.filter_objects(request.GET)}
            status = 201

        else:
            template = self.edit_template
            context = {'form': form}
            status = 400

        return render(request, template, context, status=status)

    @handle_exception
    def put(self, request, id):
        obj = self.get_object(request.user, id)
        form = self.edit_form(request.POST, instance=obj)

        if form.is_valid():
            form.save()
            template = self.list_template
            context = {'objects': self.filter_objects(request.GET)}
            status = 200

        else:
            template = self.edit_template
            context = {'form': form}
            status = 400

        return render(request, template, context, status=status)

    @handle_exception
    def delete(self, request, id):
        obj = self.get_object(request.user, id)
        obj.delete()

        return render(request, self.list_template,
                      {'objects': self.filter_objects(request.GET)}, status=204)

