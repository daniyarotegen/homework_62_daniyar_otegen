from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from tracker.forms import ProjectForm, IssueForm
from tracker.models import Project


class ProjectIndexView(ListView):
    template_name = 'projects.html'
    model = Project
    context_object_name = 'projects'
    queryset = Project.objects.order_by('start_date')


class ProjectDetailView(DetailView):
    template_name = 'project_detail.html'
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        issues = project.issues.all()
        context['issues'] = issues
        return context


class ProjectCreateView(CreateView):
    template_name = 'project_create.html'
    form_class = ProjectForm
    model = Project

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class IssueCreateProjectView(CreateView):
    template_name = 'issue_create.html'
    form_class = IssueForm

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['pk']})

    def get_initial(self):
        initial = super().get_initial()
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        initial['project'] = project
        return initial

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        return super().form_valid(form)
