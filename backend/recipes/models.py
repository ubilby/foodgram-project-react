from django.db import models

from users.models import CustomUser
from tags.models import Tag
from ingredients.models import Ingredients
from backend.validators import validate_positive


class Recipes(models.Model):
    name = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, blank=False)
    ingredients = models.ManyToManyField(
        Ingredients,
        related_name='recipes',
        through='RecipesIngredients',
        blank=False,
    )
    cooking_time = models.PositiveIntegerField()
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes_used',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )

    def __str__(self):
        return self.name


class RecipesIngredients(models.Model):
    recipes = models.ForeignKey(
        'Recipes',
        on_delete=models.CASCADE,
        related_name='ingredients_used'
    )
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='recipes_used'
    )
    amount = models.IntegerField(validators=[validate_positive])
