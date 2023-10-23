from django.db import models
from django.contrib.auth.models import AbstractUser

from backend.validators import username_validator


class Account(AbstractUser):
    username = models.SlugField(
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'
        ordering = ("username",)
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username="me"),
                name="name_not_me"
            )
        ]

    def __str__(self):
        return self.username
