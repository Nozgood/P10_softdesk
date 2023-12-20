from django.db import models
from softdesk import settings


ISSUE_PRIORITY = [
    "LOW",
    "MEDIUM",
    "HIGH"
]

class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACKEND = 'back-end'
        FRONTEND = 'front-end'
        IOS = 'iOS'
        ANDROID = "android"

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author'
    )
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=250)
    type = models.CharField(max_length=10, choices=ProjectType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributor"
    )

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="project"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'project'],
                name='unique_contributor'
            )
        ]
