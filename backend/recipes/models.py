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
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
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


class Tag(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient')
    cooking_time = models.PositiveIntegerField()
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
