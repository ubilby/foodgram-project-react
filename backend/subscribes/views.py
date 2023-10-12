from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscribe
from .serializers import SubscribeCreateSerializer, SubscribeReadSerializer
from users.models import CustomUser


class SubscribeView(ListCreateAPIView):
    serializer_class = SubscribeCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, pk):
        author_id = pk
        user_id = self.request.user.id
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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubscribeReadSerializer
        return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(subscribing__user=user)
