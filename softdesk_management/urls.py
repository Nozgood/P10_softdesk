from django.urls import path
from softdesk_management import views

app_name = "softdesk"

urlpatterns = [
    path(
        'project/create/',
        views.ProjectAPIView.as_view(),
        name='create_project'
    ),
    path(
        'project/get/<int:project_id>',
        views.ProjectAPIView.as_view(),
        name='create_project'
    ),
    path(
        'project/update/<int:project_id>',
        views.ProjectAPIView.as_view(),
        name='update_project'
    ),
    path(
        'project/delete/<int:project_id>',
        views.ProjectAPIView.as_view(),
        name='delete_project'
    ),
    path(
        'project/contribute/',
        views.ContributorAPIView.as_view(),
        name="contribute"
    ),
    path(
        'issue/create/',
        views.IssueAPIView.as_view(),
        name='create_issue'
    ),
    path(
        'issue/get/<int:issue_id>',
        views.IssueAPIView.as_view(),
        name='get_issue'
    ),
    path(
        'issue/update/<int:issue_id>',
        views.IssueAPIView.as_view(),
        name='update_issue'
    ),
    path(
        'issue/delete/<int:issue_id>',
        views.IssueAPIView.as_view(),
        name='delete_issue'
    ),
]
