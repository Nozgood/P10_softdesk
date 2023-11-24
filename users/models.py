from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.IntegerField(
        blank=False,
        help_text="âge"
    )

    can_be_contacted = models.BooleanField(
        blank=False,
        null=False,
        default=True,
        help_text="pouvons-nous vous contacter ?",
    )

    data_can_be_shared = models.BooleanField(
        blank=False,
        null=False,
        default=True,
        help_text="pouvons-nous partager vos données avec nos partenaires ?",
    )

    def __str__(self):
        return f'{self.username}'
