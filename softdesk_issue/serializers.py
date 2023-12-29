from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    IntegerField
)
from users import models as users_models
from softdesk_issue.models import Issue, Comment
from softdesk_management.models import Project
from django.utils import timezone

class IssueSerializer(ModelSerializer):
    project_id = IntegerField(min_value=1, required=True)
    attribution_id = IntegerField(required=False)

    class Meta:
        model = Issue
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
        project_id = attrs.get("project_id")
        attribution_id = attrs.get("attribution_id")
        try:
            attrs["attribution"] = users_models.User.objects.get(
                pk=attribution_id,
                contributor__project_id=project_id
            )
        except users_models.User.DoesNotExist:
            raise ValidationError(
                "the assigned used does not exists or is not a contributor"
            )
        return attrs

    def create(self, validated_data):
        reporter = self.context["request"].user
        project_id = validated_data["project_id"]
        try:
            project = Project.objects.get(
                pk=project_id
            )
        except Project.DoesNotExist:
            raise ValidationError(
                "the project you give does not exist"
            )

        validated_data["reporter"] = reporter
        validated_data["project"] = project

        return Issue.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = timezone.now()
        instance.save()
        return instance

class CommentSerializer(ModelSerializer):
    issue_id = IntegerField(min_value=1, required=True)

    class Meta:
        model = Comment
        fields = [
            "issue_id",
            "description"
        ]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = timezone.now()
        instance.save()
        return instance
