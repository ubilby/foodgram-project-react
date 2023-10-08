from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import RecipesCreateUpdateSerializer, RecipesReadSerializer
from .models import Recipes


class RecipesViewSet(ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesCreateUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesReadSerializer
        return self.serializer_class
