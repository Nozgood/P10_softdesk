from rest_framework.permissions import BasePermission
from softdesk_management.models import Contributor

class IsProjectContributor(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        project_id = view.kwargs.get('project_id')
        return Contributor.objects.filter(
            project_id=project_id,
            user=request.user
        ).exists()
