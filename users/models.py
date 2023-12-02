from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.IntegerField(
        blank=False,
    )

    can_be_contacted = models.BooleanField(
        blank=False,
        null=False,
        default=True,
    )

    data_can_be_shared = models.BooleanField(
        blank=False,
        null=False,
        default=True,
    )

    def __str__(self):
        return f'{self.username}'

class LoginUser(models.Model):
    username = models.CharField(
        max_length=150,
    )
    password = models.CharField(
        max_length=150,
    )
