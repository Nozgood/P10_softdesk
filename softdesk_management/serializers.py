from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    IntegerField
)
from users import models as users_models
from softdesk_management import models
from django.db import IntegrityError
from django.utils import timezone

class ProjectSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return models.Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.description = validated_data["description"]
        instance.type = validated_data["type"]
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
        project_id = validated_data.pop("project_id")
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


class IssueSerializer(ModelSerializer):
    project_id = IntegerField(min_value=1)
    attribution_id = IntegerField(min_value=1)

    class Meta:
        model = models.Issue
        fields = [
            "project_id",
            "name",
            "problem",
            "status",
            "priority",
            "type",
            "attribution_id",
        ]

    def create(self, validated_data):
        reporter_user = self.context["request"].user
        project_id = validated_data["project_id"]

        try:
            project = models.Project.objects.get(
                pk=project_id
            )
        except models.Project.DoesNotExist:
            raise ValidationError(
                "the project you give does not exist"
            )

        if not models.Contributor.objects.filter(
            project_id=project_id,
            user=reporter_user
        ).exists():
            raise ValidationError(
                "you must be a contributor of this project to create an issue"
            )

        try:
            attribution_user = users_models.User.objects.get(
                pk=validated_data["attribution_id"]
            )
            if not models.Contributor.objects.filter(
                project_id=project_id,
                user=attribution_user,
            ).exists():
                raise ValidationError(
                    "the user you want to assign the issue to is not "
                    "a contributor of this project"
                )
        except users_models.User.DoesNotExist:
            raise ValidationError(
                "the user you want to assign the issue to does not exist"
            )
        validated_data["attribution"] = attribution_user
        validated_data["reporter"] = reporter_user
        validated_data["project"] = project

        return models.Issue.objects.create(**validated_data)
