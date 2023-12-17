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
