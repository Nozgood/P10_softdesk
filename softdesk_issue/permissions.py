from rest_framework.permissions import BasePermission
from softdesk_management.models import Contributor
from softdesk_issue.models import Issue

class IsProjectContributorForIssue(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET" or request.method == "DELETE":
            return True

        project_id = request.data.get("project_id")
        if project_id is None:
            return False

        return Contributor.objects.filter(
            project_id=project_id,
            user=request.user
        ).exists()

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return Contributor.objects.filter(
                project_id=obj.project_id,
                user=request.user
            )

        return request.user == obj.reporter

class IsProjectContributorForComment(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET" or request.method == "DELETE":
            return True

        issue_id = request.data.get('issue_id')
        if issue_id is None:
            return False

        return Contributor.objects.filter(
            project__issue__id=issue_id,
            user=request.user
        ).exists()

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return Contributor.objects.filter(
                project__issue__id=obj.issue_id,
                user=request.user
            ).exists()

        return request.user == obj.author
