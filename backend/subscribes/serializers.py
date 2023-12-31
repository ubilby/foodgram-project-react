from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Recipes
from users.models import Account
from users.serializers import AccountSerializer

from .models import Subscribe


class SubscribeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ('author', 'user')

    def validate_author(self, value):
        user = self.context['user']
        if user == value:
            raise serializers.ValidationError(
                "Self subscribe is depricated.")
        if Subscribe.objects.filter(author=value, user=user).exists():
            raise serializers.ValidationError(
                "Can't subscribe twice on one author.")
        return value

    def to_representation(self, instance):
        return SubscribeSerializer(instance=instance.author,
                                   context=self.context).data


class SubscribeSerializer(AccountSerializer):
    recipes = serializers.SerializerMethodField()
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
            user = self.context['user']
            return (
                user.id is not None
                and user.subscriber.filter(author=obj).exists()
            )
        return True

    def get_recipes(self, obj):
        recipes_limit = self.context.get('recipes_limit')
        recipes = obj.recipes_used.all()
        if recipes_limit:
            try:
                recipes = recipes[:int(recipes_limit)]
            except TypeError:
                pass

        return ShortSerializer(recipes, many=True, context=self.context).data

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['recipes'] = self.get_recipes(instance)
        response['recipes_count'] = self.get_recipes_count(instance)
        return response


class ShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')
