from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from backend.permissions import IsAuthorOrAdminOrReadOnly

from .filter import RecipesFilterSet
from .models import Recipes
from .serializers import RecipesCreateUpdateSerializer, RecipesReadSerializer


class RecipesViewSet(ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesCreateUpdateSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilterSet

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesReadSerializer
        return self.serializer_class
