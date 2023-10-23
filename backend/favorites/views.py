from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response

from .models import Favorite
from .serializers import FavoriteSerializer
from recipes.models import Recipes
from recipes.serializers import RecipesForSubscriptionSerializer


class FavoriteView(CreateAPIView, DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    lookup_field = 'recipe__id'

    def create(self, request, pk):
        user = self.request.user.id
        recipe = get_object_or_404(Recipes, id=pk)
        request.data['user'] = user
        request.data['recipe'] = pk
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer = RecipesForSubscriptionSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.request.user
        user.favorite_recipes.filter(recipe_id=pk)[0].delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
