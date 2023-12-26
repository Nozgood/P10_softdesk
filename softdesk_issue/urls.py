from django.urls import path
from softdesk_issue.views import CommentAPIView, IssueRetrieveView, IssueCreateView, IssueUpdateView, IssueDeleteView

app_name = "softdesk_issue"

urlpatterns = [
    path(
        'issue/create/',
        IssueCreateView.as_view(),
        name='create_issue'
    ),
    path(
        'issue/<int:pk>',
        IssueRetrieveView.as_view(),
        name='get_issue'
    ),
    path(
        'issue/update/<int:pk>',
        IssueUpdateView.as_view(),
        name='update_issue'
    ),
    path(
        'issue/delete/<int:pk>',
        IssueDeleteView.as_view(),
        name='delete_issue'
    ),
    path(
        'comment/create/',
        CommentAPIView.as_view(),
        name='create_comment'
    ),
    path(
        'comment/get/<str:comment_id>',
        CommentAPIView.as_view(),
        name='get_comment'
    ),
    path(
        'comment/update/<str:comment_id>',
        CommentAPIView.as_view(),
        name='update_comment'
    ),
    path(
        'comment/delete/<str:comment_id>',
        CommentAPIView.as_view(),
        name='delete_comment'
    )
]
