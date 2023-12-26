from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from json import JSONDecodeError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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

class IssueCreateView(InstantiateIssueView, CreateAPIView):
    pass

class IssueRetrieveView(InstantiateIssueView, RetrieveAPIView):
    pass

class IssueUpdateView(InstantiateIssueView, UpdateAPIView):
    pass

class IssueDeleteView(InstantiateIssueView, DestroyAPIView):
    pass

class CommentAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsProjectContributorForComment
    ]

    @staticmethod
    def post(request):
        try:
            serializer = CommentSerializer(
                data=request.data,
                context={
                    "request": request
                }
            )
            if serializer.is_valid(raise_exception=True):
                comment = serializer.save()
                return JsonResponse(
                    {
                        "message": "success",
                        "comment_id": comment.id,
                        'link to issue': comment.issue_link
                    },
                    status=200
                )
        except JSONDecodeError:
            return JsonResponse(
                {
                    "response": "error",
                    "message": "JSON decoding error"
                },
                status=400)

    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        self.check_object_permissions(request, comment)
        return JsonResponse(
            {
                "id": comment.id,
                "author": comment.author.username,
                "description": comment.description,
                "issue_link": comment.issue_link,
                "created_at": comment.created_at,
                "updated_at": comment.updated_at
            },
            status=200
        )

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(
                {
                    "response": "success",
                    "message": "comment successfully updated"
                },
                status=200
            )

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        self.check_object_permissions(request, comment)
        comment.delete()
        return JsonResponse(
            {
                "response": "success",
                "message": "comment successfully deleted",
            },
            status=201)
