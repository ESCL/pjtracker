__author__ = 'kako'

from django.shortcuts import render
from django.views.generic import View


class StandardResourceView(View):
    list_template = None
    detail_template = None
    edit_template = None
    edit_form = None
    model = None

    def get_object(self, id):
        return self.model.objects.get(id)

    def filter_objects(self, qs):
        return self.model.objects.all(**qs)

    def get(self, request, id=None, action=None):
        if id:
            # Get object and build context
            obj = self.get_object(id)

            # Determine template and add form if required
            if action == 'edit':
                template = self.edit_template
                context = {'form': self.edit_form(instance=obj)}
            else:
                context = {'object': obj}
                template = self.detail_template

        else:
            # Template is alwatys the same
            template = self.list_template

            # Determine context based on action
            if action == 'edit':
                context= {'form': self.edit_form()}
            else:
                context = {'objects': self.filter_objects(request.GET)}

        return render(request, template, context, status=200)

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

    def put(self, request, id):
        obj = self.get_object(id)
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

    def delete(self, request, id):
        obj = self.get_object(id)
        obj.delete()

        return render(request, self.list_template,
                      {'objects': self.filter_objects(request.GET)}, status=204)
