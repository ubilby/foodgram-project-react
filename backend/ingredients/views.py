from rest_framework.viewsets import ModelViewSet

from .models import Ingredients
from .serializers import IngredientsSerializer


class IngredientsViewSet(ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
