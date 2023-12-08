from rest_framework.serializers import ModelSerializer, ValidationError
from softdesk_management.models import Project

PROJECT_TYPES = [
    "back-end",
    "front-end",
    "iOS",
    "Android"
]

class ProjectSerializer(ModelSerializer):

    def validate(self, attrs):
        project_type = attrs["type"]
        if project_type in PROJECT_TYPES:
            return attrs
        raise ValidationError(
            "You must fill a valid type: iOS, Android, back-end or front-end")

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return Project.objects.create(**validated_data)

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "type"
        ]
