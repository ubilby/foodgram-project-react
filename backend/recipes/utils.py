from django.shortcuts import get_object_or_404

from ingredients.models import Ingredients


def add_ingredient_and_amount(recipe, ingredient):
    current_ingredient_id = ingredient.get('ingredients')['id']
    current_ingredient = get_object_or_404(
        Ingredients, id=current_ingredient_id)

    amount = ingredient.get('amount')
    recipe.ingredients.add(
        current_ingredient,
        through_defaults={
            'amount': amount
        }
    )
