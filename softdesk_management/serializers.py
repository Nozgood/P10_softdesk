from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    IntegerField
)

from softdesk_management import models
from django.db import IntegrityError
from django.utils import timezone

class ProjectSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        project = models.Project.objects.create(**validated_data)
        models.Contributor.objects.create(
            project=project,
            user=self.context["request"].user
        )
        return project

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = timezone.now()
        instance.save()
        return instance

    class Meta:
        model = models.Project
        fields = [
            "name",
            "description",
            "type"
        ]

class ContributorSerializer(ModelSerializer):
    project_id = IntegerField(min_value=1)

    class Meta:
        model = models.Contributor
        fields = [
            "project_id"
        ]

    def create(self, validated_data):
        project_id = validated_data.get("project_id")
        try:
            project = models.Project.objects.get(pk=project_id)
        except models.Project.DoesNotExist:
            raise ValidationError(
                "the project you are trying to join doesn't exist"
            )

        try:
            project = models.Contributor.objects.create(
                project=project,
                user=self.context["request"].user
            )
            return project
        except IntegrityError:
            raise ValidationError(
                "you are already a contributor of this project"
            )
