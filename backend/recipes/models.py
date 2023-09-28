from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import username_validator


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = (
        (ROLE_USER, 'user'),
        (ROLE_ADMIN, 'admin'),
    )

    username = models.SlugField(
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=64,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'
        ordering = ("username",)
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username="me"), name="name_not_me"
            )
        ]

    @property
    def is_admin(self):
        return self.role == (self.ROLE_ADMIN
                             or self.is_superuser
                             or self.is_staff)

    def __str__(self):
        return self.username


class Ingredient(models.Model):
    title = models.CharField(max_length=16)


class Recipe(models.Model):
    title = models.CharField(max_length=16)
    slug = models.SlugField(max_length=50, unique=True)
    duration = models.IntegerField()
    author = models.ForeignKey(
        CustomUser, related_name='recipes',
        on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(Ingredient)
    description = models.TextField()
