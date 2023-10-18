from django.db import models

from users.models import CustomUser
from recipes.models import Recipes


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='cart_recipes')
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'cart_recipes'
