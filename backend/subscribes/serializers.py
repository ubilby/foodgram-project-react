from rest_framework import serializers

from .models import Subscribe
from recipes.serializers import RecipesForSubscriptionSerializer
from users.models import Account
from users.serializers import AccountSerializer


class SubscribeCreateSerializer(serializers.ModelSerializer):
    recipes_limit = serializers.IntegerField(
        required=False, min_value=1, allow_null=True)

    class Meta:
        model = Subscribe
        fields = ('author', 'user', 'recipes_limit')

    # def validate_author(self, value):
    #     user = self.context['request'].user
    #     if user == value:
    #         raise serializers.ValidationError(
    #             "Self subscribe is depricated.")
    #     if Subscribe.objects.filter(author=value, user=user).count() > 0:
    #         raise serializers.ValidationError(
    #             "Can't subscribe twice on one author.")
    #     return value


class SubscribeReadSerializer(serializers.ModelSerializer):
    recipes = RecipesForSubscriptionSerializer(
        many=True, source='recipes_used'
    )
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
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

    def get_is_subscribed(self, obj):
        if self.context:
            user = self.context['request'].user
            return (
                user.id is not None
                and user.subscriber.filter(author=obj).exists()
            )
        return True
