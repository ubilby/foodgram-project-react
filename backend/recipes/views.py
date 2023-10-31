from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from backend.permissions import IsAuthorOrAdminOrReadOnly

from .filter import RecipesFilterSet
from .models import Recipes
from .paganation import RecipesLimitPagination
from .serializers import RecipesCreateUpdateSerializer, RecipesReadSerializer


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
