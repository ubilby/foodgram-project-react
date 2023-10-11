from rest_framework import serializers

from .models import Subscribe
from recipes.models import Recipes
from recipes.serializers import RecipesForSubscriptionSerializer
from users.models import CustomUser
from users.serializers import CustomUserGetSerializer


class SubscribeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('author', 'user')

    def validate_author(self, value):
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError(
                "Вы не можете подписаться на себя.")
        return value


class SubscribeReadSerializer(CustomUserGetSerializer):
    recipes = RecipesForSubscriptionSerializer(
        many=True, source='recipes_used'
    )
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count"
        )

    def get_recipes_count(self, obj):
        return obj.recipes_used.count()
