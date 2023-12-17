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


class Issue(models.Model):
    class IssuePriority(models.TextChoices):
        LOW = 'LOW'
        MEDIUM = 'MEDIUM'
        HIGH = 'HIGH'

    class IssueType(models.TextChoices):
        BUG = 'BUG'
        FEATURE = 'FEATURE'
        TASK = 'TASK'

    class IssueStatus(models.TextChoices):
        TODO = 'To Do'
        IN_PROGRESS = 'In Progress'
        FINISHED = 'Finished'

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=125)
    problem = models.CharField(max_length=250)
    status = models.CharField(
        max_length=11,
        choices=IssueStatus.choices,
        default='To Do'
    )
    priority = models.CharField(max_length=6, choices=IssuePriority.choices)
    type = models.CharField(max_length=7, choices=IssueType.choices)
    reporter = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete= models.SET_NULL,
        null=True,
        related_name='reporter'
    )
    attribution = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='attribution'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
