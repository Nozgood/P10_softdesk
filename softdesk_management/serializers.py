from rest_framework.serializers import ModelSerializer
from softdesk_management.models import Project

class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "type"
        ]
