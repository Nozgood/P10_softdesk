from rest_framework.permissions import BasePermission
from softdesk_management.models import Contributor, Project, Issue

class IsProjectContributor(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        project_id = view.kwargs.get('project_id')

        return Contributor.objects.filter(
            project_id=project_id,
            user=request.user
        ).exists()


class IsProjectAuthor(BasePermission):

    def has_permission(self, request, view):
        print(request.method)
        if request.method == "POST" or request.method == "GET":
            return True

        project_id = view.kwargs.get('project_id')
        print("permission to udpate")
        try:
            project = Project.objects.get(pk=project_id)
            print(project.author == request.user)
            return project.author == request.user

        except Project.DoesNotExist:
            return False

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
