from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscribe
from .serializers import SubscribeCreateSerializer, SubscribeReadSerializer
from users.models import CustomUser


class SubscribeView(CreateAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, pk):
        author_id = self.kwargs.get('pk')
        user_id = self.request.user.id
        # author = CustomUser.objects.get(id=author_id)
        if author_id == self.request.user:
            return Response(
                {"detail": "Вы не можете подписаться на себя."},
                status=status.HTTP_400_BAD_REQUEST
            )
        request.data['author'] = author_id
        request.data['user'] = user_id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            author = get_object_or_404(CustomUser, id=author_id)
            serializer = SubscribeReadSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
