from rest_framework.viewsets import ModelViewSet

from .models import Tag
from .serializers import TagSerializer
from backend.permissions import IsAdminOrReadOnly


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = None
