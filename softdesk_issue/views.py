from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from json import JSONDecodeError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from softdesk_issue.permissions import (
    IsProjectContributorForIssue,
    IsProjectContributorForComment
)
from softdesk_issue.models import Issue
from softdesk_issue.serializers import IssueSerializer, CommentSerializer

class IssueAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsProjectContributorForIssue
    ]

    @staticmethod
    def post(request):
        try:
            serializer = IssueSerializer(
                data=request.data,
                context={
                    "request": request
                }
            )
            if serializer.is_valid(raise_exception=True):
                issue = serializer.save()
                return JsonResponse(
                    {
                        "message": "success",
                        "issue_id": issue.id
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

    def get(self, request, issue_id):
        issue = get_object_or_404(Issue, pk=issue_id)
        self.check_object_permissions(request, issue)
        return JsonResponse(
            {
                "related_project": issue.project.name,
                "reporter": issue.reporter.username,
                "assign": issue.attribution.username
                if issue.attribution else None,
                "name": issue.name,
                "description": issue.problem,
                "type": issue.type,
                "priority": issue.priority,
                "status": issue.status,
                "created_at": issue.created_at,
            },
            status=200
        )

    def put(self, request, issue_id):
        issue = get_object_or_404(Issue, pk=issue_id)
        self.check_object_permissions(request, issue)
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(
                {
                    "response": "success",
                    "message": "project successfully updated"
                },
                status=200
            )

    def delete(self, request, issue_id):
        issue = get_object_or_404(Issue, pk=issue_id)
        self.check_object_permissions(request, issue)
        issue.delete()
        return JsonResponse(
            {
                "response": "success",
                "message": "project successfully deleted",
            },
            status=200)

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

    def get(self, request):
        pass

    def update(self, request):
        pass

    def delete(self, request):
        pass
