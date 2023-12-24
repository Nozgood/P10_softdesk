from django.db import models
from softdesk import settings
from softdesk_management.models import Project
import uuid

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
        on_delete=models.CASCADE,
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

class Comment(models.Model):

    @property
    def issue_link(self):
        return settings.BASE_URL + 'api/issue/' + str(self.issue_id)

    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )
    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
