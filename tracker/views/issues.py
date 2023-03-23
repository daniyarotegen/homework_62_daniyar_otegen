from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, UpdateView, CreateView, TemplateView
from tracker.forms import IssueForm
from tracker.models import Issue
from tracker.permissions import user_in_issue_project, user_in_project


class IssueDetailView(TemplateView):
    template_name = 'issue_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        issue = get_object_or_404(Issue, pk=kwargs['pk'])
        context['issue'] = issue
        if issue.type.exists():
            context['types'] = issue.type.all()
        else:
            context['types'] = []
        return context


class IssueCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'issue_create.html'
    form_class = IssueForm
    success_message = 'Issue was created!'

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})

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

    def form_valid(self, form):
        project = self.get_object()
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        return super().form_valid(form)


class IssueUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'issue_update.html'
    form_class = IssueForm
    model = Issue
    success_message = 'Issue was updated!'

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})

    def get_permission_required(self):
        if self.request.user.groups.filter(name='Project Manager').exists():
            return 'tracker.change_issue'
        elif self.request.user.groups.filter(name='Team Lead').exists():
            return 'tracker.change_issue'
        elif self.request.user.groups.filter(name='Developer').exists():
            return 'tracker.change_issue'
        return None

    def has_permission(self):
        permission = self.get_permission_required()
        if permission is None:
            return False
        return self.request.user.has_perm(permission) and user_in_issue_project(self.request.user, self.get_object())


class IssueDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'issue_delete.html'
    model = Issue
    success_url = reverse_lazy('index')
    success_message = 'Issue was deleted!'

    def get_permission_required(self):
        if self.request.user.groups.filter(name='Project Manager').exists():
            return 'tracker.change_issue'
        elif self.request.user.groups.filter(name='Team Lead').exists():
            return 'tracker.change_issue'
        return None

    def has_permission(self):
        permission = self.get_permission_required()
        if permission is None:
            return False
        return self.request.user.has_perm(permission) and user_in_issue_project(self.request.user, self.get_object())

