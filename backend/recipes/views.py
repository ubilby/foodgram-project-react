from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .serializers import RecipesCreateUpdateSerializer, RecipesReadSerializer
from .models import Recipes
from backend.permissions import IsAuthorOrAdminOrReadOnly


class RecipesViewSet(ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesCreateUpdateSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesReadSerializer
        return self.serializer_class

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = RecipesReadSerializer(instance=serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            instance.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        updated_instance = RecipesReadSerializer(instance)
        return Response(updated_instance.data)

    def get_queryset(self):
        queryset = Recipes.objects.all()

        limit = self.request.query_params.get('limit')
        if limit:
            queryset = queryset[:int(limit)]

        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited:
            user = self.request.user
            if user.is_authenticated and is_favorited.lower() == 'true':
                queryset = queryset.filter(favorites__user=user)

        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        if is_in_shopping_cart:
            user = self.request.user
            if user.is_authenticated and is_in_shopping_cart.lower() == 'true':
                queryset = queryset.filter(cart__user=user)

        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author__id=author_id)

        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__slug__in=tags)
        return queryset
