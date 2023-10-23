from django.db.models import Q
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

    # def http_method_not_allowed(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(Q(name__istartswith=name))
        return queryset
