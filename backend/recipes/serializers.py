from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer

from ingredients.serializers import IngredientM2MSerializer, RecipesIngrdientsReadSerializer
from ingredients.models import Ingredients
from .models import Recipes
from users.serializers import CustomUserGetSerializer


class RecipesCreateUpdateSerializer(ModelSerializer):
    ingredients = IngredientM2MSerializer(many=True, source='ingredients_used')
    # image = ImageField(required=True)

    class Meta:
        model = Recipes
        fields = (
            'ingredients',
            'tags',
            # 'image',
            'name',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients_used')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(
            author=self.context['request'].user, **validated_data)
        for i in ingredients:
            current_ingredient_id = i.get('ingredients')['id']
            current_ingredient = get_object_or_404(
                Ingredients, id=current_ingredient_id)
            amount = i.get('amount')
            recipe.ingredients.add(
                current_ingredient,
                through_defaults={
                    'amount': amount
                }
            )

        recipe.tags.set(tags)
        return recipe


class RecipesReadSerializer(ModelSerializer):
    ingredients = RecipesIngrdientsReadSerializer(
        many=True,
        source='ingredients_used'
    )
    author = CustomUserGetSerializer()

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            # 'image',
            'text',
            'cooking_time'
        )
        depth = 2
