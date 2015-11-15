
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory

from ..common.views.base import StandardResourceView
from .forms import ProjectForm, ActivityForm, ProjectSearchForm, ActivitySearchForm, ActivityInlineForm, ActivityInlineFormSet
from .models import Project, Activity


class ProjectView(StandardResourceView):
    model = Project
    list_template = 'projects.html'
    detail_template = 'project.html'
    edit_template = 'project-edit.html'
    search_form = ProjectSearchForm
    main_form = ProjectForm


class ActivityView(StandardResourceView):
    model = Activity
    list_template = 'activities.html'
    detail_template = 'activity.html'
    edit_template = 'activity-edit.html'
    search_form = ActivitySearchForm
    main_form = ActivityForm


class ProjectWBSView(StandardResourceView):
    """
    Experimental WBS edit view.
    """
    model = Project
    edit_template = 'wbs-edit.html'
    formset = inlineformset_factory(Project, Activity, formset=ActivityInlineFormSet,
                                    form=ActivityInlineForm, extra=1)

    def show_forms(self, request, pk):
        """
        Render the formset for the given project.
        """
        proj = pk and self.get_object(request.user, pk) or None
        context = {'project': proj, 'forms': self.formset(instance=proj)}
        return render(request, self.edit_template, context)

    def upsert_instance(self, request, pk, **kwargs):
        """
        Save the main form (and subform is the instance is not new) and redirect
        to the collection view.
        """
        proj = pk and self.get_object(request.user, pk) or None
        context = {'project': proj}
        fs = self.formset(request.POST, instance=proj)
        context['sub_forms'] = fs

        if fs.is_valid():
            # If all defined forms are valid, save them
            instances = fs.save()
            fs.save_parents()
            Activity.objects.filter(id__in=[a.id for a in instances]).update(project=proj, owner=proj.owner)

            # Now redirect to collection view, passing kwargs (subresources work too)
            return redirect('project', pk=pk, **kwargs)

        else:
            # Invalid, render forms again with errors
            return render(request, self.edit_template, context, status=400)