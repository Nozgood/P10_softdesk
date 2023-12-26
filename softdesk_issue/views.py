from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView
)

from softdesk_issue.permissions import (
    IsProjectContributorForIssue,
    IsProjectContributorForComment
)
from softdesk_issue.models import Issue, Comment
from softdesk_issue.serializers import IssueSerializer, CommentSerializer

class InstantiateIssueView(GenericAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectContributorForIssue]

class InstantiateCommentView(GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
        IsProjectContributorForComment
    ]

class IssueCreateView(InstantiateIssueView, CreateAPIView):
    pass

class IssueRetrieveView(InstantiateIssueView, RetrieveAPIView):
    pass

class IssueUpdateView(InstantiateIssueView, UpdateAPIView):
    pass

class IssueDeleteView(InstantiateIssueView, DestroyAPIView):
    pass

class IssueListView(InstantiateIssueView, ListAPIView):

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.request.query_params.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)

        return queryset

class CommentCreateView(InstantiateCommentView, CreateAPIView):
    pass

class CommentGetView(InstantiateCommentView, RetrieveAPIView):
    pass

class CommentUpdateView(InstantiateCommentView, UpdateAPIView):
    pass

class CommentDeleteView(InstantiateCommentView, DestroyAPIView):
    pass

class CommentListView(InstantiateCommentView, ListAPIView):

    def get_queryset(self):
        queryset = Comment.objects.all()
        issue_id = self.request.query_params.get('issue_id')
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)

        return queryset
