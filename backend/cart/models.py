from django.db import models

from recipes.models import Recipes
from users.models import Account


class Cart(models.Model):
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='cart_recipes')
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name='cart')

    class Meta:
        default_related_name = 'cart_recipes'
