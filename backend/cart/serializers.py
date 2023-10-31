from rest_framework import serializers

from .models import Cart


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('user', 'recipe')

    def create(self, validated_data):
        user = validated_data.get('user')
        recipe = validated_data.get('recipe')
        return Cart.objects.create(user=user, recipe=recipe)

    def validate_recipe(self, recipe):
        user = self.context['request'].user
        if Cart.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                "Can't add twice to cart.")
        return recipe
