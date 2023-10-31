from django.db import models

from recipes.models import Recipes
from users.models import Account


class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'cart'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_recipe_in_cart')
        ]
