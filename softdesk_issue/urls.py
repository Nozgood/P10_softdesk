from django.urls import path
from softdesk_issue.views import IssueAPIView, CommentAPIView

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
    ),
    # path(
    #     'issue/comments/',
    #     IssueAPIView.as_view(),
    #     name='list_comments'
    # ),
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
