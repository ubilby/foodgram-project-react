from django.db import models

from users.models import CustomUser
from recipes.models import Recipes


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='favorite_recipes')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
