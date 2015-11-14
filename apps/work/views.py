
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from ..common.views.base import StandardResourceView
from .forms import ProjectForm, ActivityForm, ProjectSearchForm, ActivitySearchForm, ActivityInlineForm
from .models import Project, Activity


class ProjectView(StandardResourceView):
    model = Project
    list_template = 'projects.html'
    detail_template = 'project.html'
    edit_template = 'project-edit.html'
    search_form = ProjectSearchForm
    main_form = ProjectForm
    sub_forms = inlineformset_factory(Project, Activity, form=ActivityInlineForm)

    def show_forms(self, request, pk):
        """
        Render the main form and subform for the given instance pk.
        """
        proj = pk and self.get_object(request.user, pk) or None
        main_form = self.main_form(instance=proj, user=request.user, prefix='main')
        context = {'project': proj, 'main_form': main_form}

        form_set = self.sub_forms(instance=proj)
        context['sub_forms'] = form_set

        return render(request, self.edit_template, context)

    def upsert_instance(self, request, pk, **kwargs):
        """
        Save the main form (and subform is the instance is not new) and redirect
        to the collection view.
        """
        proj = pk and self.get_object(request.user, pk) or None
        main_form = self.main_form(request.POST, instance=proj, user=request.user, prefix='main')
        context = {'project': proj, 'main_form': main_form}

        form_set = self.sub_forms(request.POST, instance=proj)
        context['sub_forms'] = form_set

        if main_form.is_valid() and form_set.is_valid():
            # If all defined forms are valid, save them
            main_form.save()
            instances = form_set.save()
            Activity.objects.filter(id__in=[a.id for a in instances]).update(project=proj, owner=proj.owner)

            # Now redirect to collection view, passing kwargs (subresources work too)
            view_name = self.collection_view_name or self.model._meta.verbose_name_plural.lower().replace(' ', '')
            return redirect(view_name, **kwargs)

        else:
            # Invalid, render forms again with errors
            return render(request, self.edit_template, context, status=400)


class ActivityView(StandardResourceView):
    model = Activity
    list_template = 'activities.html'
    detail_template = 'activity.html'
    edit_template = 'activity-edit.html'
    search_form = ActivitySearchForm
    main_form = ActivityForm
