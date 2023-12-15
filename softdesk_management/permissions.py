from rest_framework.permissions import BasePermission
from softdesk_management.models import Contributor, Project, Issue

class IsProjectContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(
            project=obj,
            user=request.user
        ).exists()


class IsProjectAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        return obj.author == request.user

class IsProjectIssueContributor(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        issue_id = view.kwargs.get('issue_id')
        try:
            issue = Issue.objects.get(
                pk=issue_id
            )
            project = issue.project
            return Contributor.objects.filter(
                project=project,
                user=request.user
            ).exists()
        except Issue.DoesNotExist:
            return False
