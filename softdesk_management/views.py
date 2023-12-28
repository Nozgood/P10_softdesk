from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView
)

from softdesk_management.serializers import (
    ProjectSerializer,
    ContributorSerializer
)
from softdesk_management.models import Contributor, Project
from softdesk_management.permissions import (
    IsProjectContributor,
    IsProjectAuthor
)

class InstantiateProjectView(GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [
        IsAuthenticated,
        IsProjectContributor,
        IsProjectAuthor
    ]

class ProjectCreateView(InstantiateProjectView, CreateAPIView):
    pass

class ProjectGetView(InstantiateProjectView, RetrieveAPIView):
    pass

class ProjectUpdateView(InstantiateProjectView, UpdateAPIView):
    pass

class ProjectDeleteView(InstantiateProjectView, DestroyAPIView):
    pass

class ProjectListView(InstantiateProjectView, ListAPIView):

    def get_queryset(self):
        queryset = Project.objects.all()
        checked_queryset = []
        for project in queryset:
            if Contributor.objects.filter(
                project=project,
                user=self.request.user
            ).exists():
                checked_queryset.append(project)
        return checked_queryset

class ContributorCreateView(CreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
