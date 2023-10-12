from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Favorite
from recipes.serializers import RecipesReadSerializer
from recipes.models import Recipes
from users.models import CustomUser


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def create(self, validated_data):
        user = validated_data.get('user')
        recipe = validated_data.get('recipe')
        return Favorite.objects.create(user=user, recipe=recipe)
