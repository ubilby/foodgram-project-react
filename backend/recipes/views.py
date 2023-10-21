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
        return Response(instance.data, status=status.HTTP_201_CREATED, headers=headers)
