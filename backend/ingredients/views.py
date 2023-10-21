from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Ingredients
from .serializers import IngredientsSerializer
from backend.permissions import IsAdminOrReadOnly


class IngredientsViewSet(ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    permission_classes = [IsAdminOrReadOnly, ]

    def http_method_not_allowed(self, request, *args, **kwargs):
        """
        Переопределяем метод для возвращения 405 Method Not Allowed
        вместо 403 Forbidden.
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
