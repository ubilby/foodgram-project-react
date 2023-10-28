from rest_framework import serializers
from djoser.serializers import UserSerializer

from .models import Account


class AccountSerializer(UserSerializer):
    username = serializers.RegexField(
        regex=r'[\w.@+z-]+\Z',
        max_length=150,
        required=True,
    )
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed'
        )
        model = Account

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'id': instance.id,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'is_subscribed': self.get_is_subscribed(instance),
        }

    def get_is_subscribed(self, obj):
        if self.context:
            user = self.context['request'].user
            return (
                user.id is not None
                and user.subscriptions.filter(id=obj.id).exists()
            )
        return True


class SubscribesSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes_count',
            'recipes',
        )
        model = Account

    def get_recipes(self, obj):
        from recipes.serializers import RecipesForSubscriptionSerializer
        recipes = obj.recipes_used.all()
        return RecipesForSubscriptionSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes_used.all().count()

    def get_is_subscribed(self, obj):
        if self.context:
            user = self.context['request'].user
            return (
                user.id is not None
                and user.subscriptions.filter(id=obj.id).exists()
            )
        return True
