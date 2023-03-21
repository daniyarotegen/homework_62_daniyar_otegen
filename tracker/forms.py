from django import forms
from django.core.validators import BaseValidator
from .models import Issue, Type, Status, Project


class CustomMaxValidator(BaseValidator):
    def __init__(self, limit_value=50):
        message = 'Maximum summary length is %(limit_value)s symbols. You entered %(show_value)s symbols'
        super().__init__(limit_value=limit_value, message=message)

    def compare(self, value, limit_value):
        return limit_value < value

    def clean(self, x):
        return len(x)


class CustomMinValidator(BaseValidator):
    def __init__(self, limit_value=2):
        message = 'Minimum summary length is %(limit_value)s symbols. You entered %(show_value)s symbols'
        super().__init__(limit_value=limit_value, message=message)

    def compare(self, value, limit_value):
        return limit_value > value

    def clean(self, x):
        return len(x)


class IssueForm(forms.ModelForm):
    summary = forms.CharField(
        validators=(CustomMaxValidator(), CustomMinValidator()))

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'project', 'status', 'type']
        labels = {
            'summary': 'Summary',
            'description': 'Description',
            'project': 'Project',
            'status': 'Status',
            'type': 'Type'
        }

    project = forms.ModelChoiceField(queryset=Project.objects.all())
    status = forms.ModelChoiceField(queryset=Status.objects.all())
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all())


class SearchForm(forms.Form):
    search = forms.CharField(max_length=20, required=False, label='Search')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']
        labels = {
            'name': 'Name',
            'description': 'Description',
            'start_date': 'Start Date',
            'end_date': 'End Date'
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'})
        }
