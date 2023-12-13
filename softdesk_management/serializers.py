from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    IntegerField
)
from softdesk_management.models import Project, Contributor
from django.db import IntegrityError
from django.utils import timezone

class ProjectSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.description = validated_data["description"]
        instance.type = validated_data["type"]
        instance.updated_at = timezone.now()
        instance.save()
        return instance

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "type"
        ]

class ContributorSerializer(ModelSerializer):
    project_id = IntegerField(min_value=1)

    class Meta:
        model = Contributor
        fields = [
            "project_id"
        ]

    def create(self, validated_data):
        project_id = validated_data.pop("project_id")
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise ValidationError(
                "the project you are trying to join doesn't exist"
            )

        try:
            project = Contributor.objects.create(
                project=project,
                user=self.context["request"].user
            )
            return project
        except IntegrityError:
            raise ValidationError(
                "you are already a contributor of this project"
            )
