from rest_framework.permissions import BasePermission
from softdesk_management.models import Contributor

class IsProjectContributorForIssue(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        project_id = request.data.get("project_id")
        if project_id is None:
            return False

        return Contributor.objects.filter(
            project_id=project_id,
            user=request.user
        )

    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(
            project_id=obj.project_id,
            user=request.user
        )
