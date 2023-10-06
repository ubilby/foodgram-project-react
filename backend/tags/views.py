from rest_framework import viewsets
from .models import Tag
from .serializers import TagSerializer
from api.permissions import IsAdminOrReadOnly


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly, ]
