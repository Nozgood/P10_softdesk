from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    CharField
)
from softdesk_management.models import Project, Contributor

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

class ContributorSerializer(ModelSerializer):
    project_name = CharField(max_length=150)

    class Meta:
        model = Contributor
        fields = [
            "project_name"
        ]

    def create(self, validated_data):
        project_name = validated_data.pop("project_name")
        try:
            project = Project.objects.get(name=project_name)
        except Project.DoesNotExist:
            raise ValidationError(
                "the project you are trying to join doesn't exist"
            )
        return Contributor.objects.create(
            project=project,
            user=self.context["request"].user
        )
