from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import username_validator


class CustomUser(AbstractUser):
    LOGIN_FIELD = 'login'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = (
        (ROLE_USER, 'user'),
        (ROLE_ADMIN, 'admin'),
    )

    login = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator]
    )
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=64,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    confirmation_code = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Юзеры'
        verbose_name_plural = 'Юзеры'
        ordering = ("login",)
        constraints = [
            models.CheckConstraint(
                check=~models.Q(login="me"), name="name_not_me"
            )
        ]

    @property
    def is_admin(self):
        return self.role == (self.ROLE_ADMIN
                             or self.is_superuser
                             or self.is_staff)

    def __str__(self):
        return self.login
