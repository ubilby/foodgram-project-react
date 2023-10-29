import os

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     RetrieveAPIView)
from rest_framework.response import Response

from recipes.models import Recipes, RecipesIngredients
from recipes.serializers import RecipesForSubscriptionSerializer

from .models import Cart
from .serializers import CartSerializer


class CartView(CreateAPIView, DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
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
        user.cart_recipes.filter(recipe_id=pk)[0].delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        file_name = self.create_file(user)
        data = self.create_data(user)
        self.fill_file(file_name, data)
        response = FileResponse(open(file_name, "rb"))
        response['Content-Disposition'] = (
            f'attachment;filename="{os.path.basename(file_name)}'
        )
        os.remove(file_name)
        return response

    def create_data(self, user):
        ingredients = RecipesIngredients.objects.filter(
            recipes__cart_recipes__user_id=user.id
        ).values(
            'ingredients__name', 'ingredients__measurement_unit'
        ).annotate(total_amount=Sum('amount'))

        data = [[
                item['ingredients__name'],
                item['total_amount'],
                item['ingredients__measurement_unit']
                ] for item in ingredients
                ]
        return data

    def create_file(self, user):
        file_name = f'{user}.txt'
        with open(file_name, 'w') as file:
            file.write('ingredient, amount, measurement_unit\n')
        return file_name

    def fill_file(self, file_name, data):
        for ingredient, amount, measurement_unit in data:
            with open(file_name, 'a') as file:
                file.write(f'{ingredient}, {amount}, {measurement_unit}\n')
