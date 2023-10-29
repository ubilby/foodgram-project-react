from django.db import models

from backend.validators import validate_positive
from ingredients.models import Ingredients
from tags.models import Tag
from users.models import Account


class Recipes(models.Model):
    name = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, blank=False)
    ingredients = models.ManyToManyField(
        Ingredients,
        related_name='recipes',
        through='RecipesIngredients',
        blank=False,
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[validate_positive]
    )
    text = models.TextField()
    author = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='recipes_used',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']

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
