from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from backend.permissions import IsAuthorOrAdminOrReadOnly

from .filter import RecipesFilterSet
from .models import Recipes
from .serializers import RecipesCreateUpdateSerializer, RecipesReadSerializer
from .paganation import RecipesLimitPagination


class RecipesViewSet(ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesCreateUpdateSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilterSet
    pagination_class = RecipesLimitPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesReadSerializer
        return self.serializer_class
