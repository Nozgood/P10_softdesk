from django.urls import path
from softdesk_issue.views import IssueAPIView

app_name = "softdesk_issue"

urlpatterns = [
    path(
        'issue/create/',
        IssueAPIView.as_view(),
        name='create_issue'
    ),
    path(
        'issue/get/<int:issue_id>',
        IssueAPIView.as_view(),
        name='get_issue'
    ),
    path(
        'issue/update/<int:issue_id>',
        IssueAPIView.as_view(),
        name='update_issue'
    ),
    path(
        'issue/delete/<int:issue_id>',
        IssueAPIView.as_view(),
        name='delete_issue'
    )
]
