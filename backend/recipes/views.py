from rest_framework.viewsets import ModelViewSet

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
