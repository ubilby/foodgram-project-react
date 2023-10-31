from rest_framework import serializers

from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def create(self, validated_data):
        user = validated_data.get('user')
        recipe = validated_data.get('recipe')
        return Favorite.objects.create(user=user, recipe=recipe)

    def validate_recipe(self, recipe):
        user = self.context['request'].user
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                "Can't add twice to favorites.")
        return recipe
