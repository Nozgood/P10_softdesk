from django.urls import path
from softdesk_issue import views

app_name = "softdesk_issue"

urlpatterns = [
    path(
        'issue/create/',
        views.IssueCreateView.as_view(),
        name='create_issue'
    ),
    path(
        'issue/<int:pk>',
        views.IssueRetrieveView.as_view(),
        name='get_issue'
    ),
    path(
        'issues/',
        views.IssueListView.as_view(),
        name='list_issues'
    ),
    path(
        'issue/update/<int:pk>',
        views.IssueUpdateView.as_view(),
        name='update_issue'
    ),
    path(
        'issue/delete/<int:pk>',
        views.IssueDeleteView.as_view(),
        name='delete_issue'
    ),
    path(
        'comment/create/',
        views.CommentCreateView.as_view(),
        name='create_comment'
    ),
    path(
        'comment/get/<str:comment_id>',
        views.CommentGetView.as_view(),
        name='get_comment'
    ),
    path(
        'comment/update/<str:comment_id>',
        views.CommentUpdateView.as_view(),
        name='update_comment'
    ),
    path(
        'comment/delete/<str:comment_id>',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),
    path(
        'comments/',
        views.CommentListView.as_view(),
        name='list_comments'
    )
]
