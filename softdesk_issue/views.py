from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from json import JSONDecodeError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from softdesk_issue.permissions import (
    IsProjectContributorForIssue
)
from softdesk_issue.models import Issue
from softdesk_issue.serializers import IssueSerializer

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

    @staticmethod
    def get(request, issue_id):
        issue = get_object_or_404(Issue, pk=issue_id)
        return JsonResponse(
            {
                "related_project": issue.project.name,
                "reporter": issue.reporter.username,
                "assign": issue.attribution.username,
                "name": issue.name,
                "description": issue.problem,
                "type": issue.type,
                "priority": issue.priority,
                "status": issue.status,
                "created_at": issue.created_at,
            },
            status=200
        )