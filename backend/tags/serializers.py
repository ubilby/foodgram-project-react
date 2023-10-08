from rest_framework import serializers
from .models import Tag
# from recipes.models import RecipesTag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


# class TagM2MSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(
#         source='tag.id'
#     )

#     class Meta:
#         model = RecipesTag
#         fields = (
#             'id',
#         )
#         read_only_fields = ('id', )
