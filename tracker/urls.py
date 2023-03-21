from django.urls import path
from tracker.views.index import IndexView
from tracker.views.issues import IssueDetailView, IssueCreateView, IssueUpdateView, IssueDeleteView
from tracker.views.projects import ProjectIndexView, ProjectCreateView, ProjectDetailView, IssueCreateProjectView

urlpatterns = [
    path("", IndexView.as_view(), name='index'),
    path("issue/add", IssueCreateView.as_view(), name='issue_create'),
    path("issue/<int:pk>", IssueDetailView.as_view(), name='issue_detail'),
    path('issue/<int:pk>/update/', IssueUpdateView.as_view(), name='issue_update'),
    path('issue/<int:pk>/delete/', IssueDeleteView.as_view(), name='issue_delete'),
    path('issue/<int:pk>/confirm_delete/', IssueDeleteView.as_view(), name='confirm_delete'),
    path('projects', ProjectIndexView.as_view(), name='project_index'),
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/issue/create/', IssueCreateProjectView.as_view(), name='issue_create_project'),

]