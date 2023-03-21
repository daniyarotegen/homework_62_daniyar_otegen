from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, UpdateView, CreateView, TemplateView
from tracker.forms import IssueForm
from tracker.models import Issue


class IssueCreateView(CreateView):
    template_name = 'issue_create.html'
    model = Issue
    form_class = IssueForm

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})


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


class IssueUpdateView(UpdateView):
    template_name = 'issue_update.html'
    form_class = IssueForm
    model = Issue

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})


class IssueDeleteView(DeleteView):
    template_name = 'issue_delete.html'
    model = Issue
    success_url = reverse_lazy('index')
