import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (ImageField, ModelSerializer,
                                        SerializerMethodField, ValidationError)

from ingredients.serializers import (IngredientM2MSerializer,
                                     RecipesIngrdientsReadSerializer)
from ingredients.models import Ingredients
from .models import Recipes, RecipesIngredients
from users.serializers import AccountGetSerializer
from favorites.models import Favorite
from cart.models import Cart


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipesCreateUpdateSerializer(ModelSerializer):
    ingredients = IngredientM2MSerializer(
        many=True, source='ingredients_used', required=True
    )
    image = Base64ImageField(required=True)
    image_url = SerializerMethodField(
        'get_image_url',
    )

    class Meta:
        model = Recipes
        fields = (
            'ingredients',
            'tags',
            'image',
            'image_url',
            'name',
            'text',
            'cooking_time'
        )

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

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

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients_used', [])
        self.validate_ingredients(ingredients)
        tags_data = validated_data.pop('tags', [])
        self.validate_tags(tags_data)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)

        for recive_ingredient in ingredients:
            ingredient_id = recive_ingredient.get('ingredients').get('id')
            ingredient = Ingredients.objects.get(pk=ingredient_id)
            amount = recive_ingredient.get('amount')
            obj, created = RecipesIngredients.objects.update_or_create(
                recipes=instance,
                ingredients=ingredient,
                defaults={'amount': amount}
            )
        instance.tags.set(tags_data)
        instance.save()

        return instance

    def validate_ingredients(self, values):
        if not values:
            raise ValidationError(
                'Ingredients list cannot be empty.')
        unique_ids = set()
        for value in values:
            id = value['ingredients']['id']
            if id in unique_ids:
                raise ValidationError(
                    'Ingredients should be unique.'
                )
            if Ingredients.objects.filter(id=id).count() == 0:
                raise ValidationError('Non existing ingredient')
            unique_ids.add(id)
        return values

    def validate_tags(self, values):
        if not values:
            raise ValidationError('Tags field is required')
        unique_ids = set()
        for tag_id in values:
            if tag_id in unique_ids:
                raise ValidationError(
                    'Tags should be unique.')
            unique_ids.add(tag_id)
        return values


class RecipesReadSerializer(ModelSerializer):
    ingredients = RecipesIngrdientsReadSerializer(
        many=True,
        source='ingredients_used',
        required=True
    )
    author = AccountGetSerializer()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        depth = 2

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_is_in_shopping_cart(self, obj):
        if self.context:
            user = self.context['request'].user
            if (
                self.context['request'].user.is_authenticated
                and Cart.objects.filter(user=user, recipe=obj).count()
            ):
                return True
        return False

    def get_is_favorited(self, obj):
        if self.context:
            user = self.context['request'].user
            if (
                self.context['request'].user.is_authenticated
                and Favorite.objects.filter(user=user, recipe=obj).count()
            ):
                return True
        return False


class RecipesForSubscriptionSerializer(ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')
