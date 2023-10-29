from django.db import models

from recipes.models import Recipes
from users.models import Account


class Favorite(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='favorite_recipes')
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name='favorites')
