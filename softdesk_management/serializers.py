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
    project_id = IntegerField(min_value=1, required=True)
    attribution_id = IntegerField(allow_null=True, required=False)

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

    def validate(self, attrs):
        reporter = self.context["request"].user
        project_id = attrs.get("project_id")
        attribution_id = attrs.get("attribution_id")

        if not models.Project.objects.filter(
            pk=project_id
        ).exists():
            raise ValidationError("this project does not exist")

        if not models.Contributor.objects.filter(
            project_id=project_id,
            user=reporter
        ).exists():
            raise ValidationError(
                "you must be a contributor of this project to create an issue"
            )

        if attribution_id is not None and users_models.User.objects.filter(
            pk=attribution_id
        ).exists() is False:
            raise ValidationError(
                "the assigned used does not exists"
            )

        if attribution_id is not None and models.Contributor.objects.filter(
                project_id=project_id,
                user_id=attribution_id,
        ).exists() is False:
            raise ValidationError(
                "the user you want to assign the issue to is not "
                "a contributor of this project"
            )

        return attrs

    def create(self, validated_data):
        reporter = self.context["request"].user
        project_id = validated_data["project_id"]
        attribution_id = validated_data.get('attribution_id', None)
        try:
            project = models.Project.objects.get(
                pk=project_id
            )
            if attribution_id is not None:
                assigned_user = users_models.User.objects.get(
                    pk=attribution_id
                )
                validated_data["attribution"] = assigned_user
        except models.Project.DoesNotExist:
            raise ValidationError(
                "the project you give does not exist"
            )
        except users_models.User.DoesNotExist:
            raise ValidationError(
                "the user you want to assign the issue to does not exist"
            )

        validated_data["reporter"] = reporter
        validated_data["project"] = project

        return models.Issue.objects.create(**validated_data)
