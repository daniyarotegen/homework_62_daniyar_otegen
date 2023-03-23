from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from tracker.forms import ProjectForm, IssueForm, ProjectUserForm
from tracker.models import Project
from tracker.permissions import user_in_project


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


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'project_create.html'
    form_class = ProjectForm
    model = Project
    success_message = 'Project was created!'

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()
        project.users.add(self.request.user)
        project.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})

    def get_permission_required(self):
        return 'tracker.add_project' if self.request.user.groups.filter(name='Project Manager').exists() else None

    def has_permission(self):
        permission = self.get_permission_required()
        if permission is None:
            return False
        return self.request.user.has_perm(permission)


class IssueCreateProjectView(PermissionRequiredMixin, CreateView):
    template_name = 'issue_create.html'
    form_class = IssueForm
    success_message = 'Issue was created!'

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['pk']})

    def get_permission_required(self):
        if self.request.user.groups.filter(name='Project Manager').exists():
            return 'tracker.add_issue'
        elif self.request.user.groups.filter(name='Team Lead').exists():
            return 'tracker.add_issue'
        elif self.request.user.groups.filter(name='Developer').exists():
            return 'tracker.add_issue'
        return None

    def has_permission(self):
        permission = self.get_permission_required()
        if permission is None:
            return False
        return self.request.user.has_perm(permission) and user_in_project(self.request.user, self.get_object())

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


class ProjectUserView(PermissionRequiredMixin, UpdateView):
    template_name = 'project_users.html'
    form_class = ProjectUserForm
    model = Project
    success_message = 'Project users were updated!'

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})

    def get_permission_required(self):
        if self.request.user.groups.filter(name='Project Manager').exists():
            return 'tracker.change_project'
        elif self.request.user.groups.filter(name='Team Lead').exists():
            return 'tracker.change_project'
        return None

    def has_permission(self):
        permission = self.get_permission_required()
        if permission is None:
            return False
        project_user_check = user_in_project(self.request.user, self.get_object())
        print(f"user_in_project: {project_user_check}")
        return self.request.user.has_perm(permission) and user_in_project(self.request.user, self.get_object())


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'project_update.html'
    form_class = ProjectForm
    model = Project
    success_message = 'Project was updated!'

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})

    def get_permission_required(self):
        return 'tracker.change_project' if self.request.user.groups.filter(name='Project Manager').exists() else None

    def has_permission(self):
        permission = self.get_permission_required()
        if permission is None:
            return False
        return self.request.user.has_perm(permission) and user_in_project(self.request.user, self.get_object())


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'project_delete.html'
    model = Project
    success_url = reverse_lazy('index')
    success_message = 'Project was deleted!'

    def get_permission_required(self):
        return 'tracker.delete_project' if self.request.user.groups.filter(name='Project Manager').exists() else None

    def has_permission(self):
        permission = self.get_permission_required()
        if permission is None:
            return False
        if self.request.user.groups.filter(name='Project Manager').exists():
            return self.request.user.has_perm(permission)
        return self.request.user.has_perm(permission) and user_in_project(self.request.user, self.get_object())


