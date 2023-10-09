from rest_framework.serializers import (
    CharField, IntegerField, ModelSerializer,
    ReadOnlyField
)
from .models import Ingredients
from recipes.models import RecipesIngredients


class IngredientsSerializer(ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name')


class IngredientM2MSerializer(ModelSerializer):
    id = IntegerField(
        source='ingredients.id'
    )

    class Meta:
        model = RecipesIngredients
        fields = (
            'id',
            'amount',
        )
        read_only_fields = ('id', )


class RecipesIngrdientsReadSerializer(ModelSerializer):
    id = IntegerField(source='ingredients.id')
    name = CharField(source='ingredients.name')
    amount = ReadOnlyField()
    measurement_unit = CharField(source='ingredients.measurement_unit')

    class Meta:
        model = RecipesIngredients
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )
