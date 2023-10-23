from django.db import models

from users.models import Account
from recipes.models import Recipes


class Favorite(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='favorite_recipes')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
