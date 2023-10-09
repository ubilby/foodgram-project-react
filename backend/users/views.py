from users.serializers import ChangePasswordSerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import CustomUser, Subscribe
from .serializers import (CustomUserSerializer,
                          CustomUserGetSerializer, SubscribeSerializer)
from .permission import IsAuthenticatedOrReadOnlyAndNoDetail


class UserProfileView(RetrieveAPIView):
    serializer_class = CustomUserGetSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user


class UserCreateView(ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny, ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomUserSerializer
        return CustomUserGetSerializer


class ChangePasswordView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)


class SubscribeView(CreateAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        author_id = self.kwargs.get('id')
        author = CustomUser.objects.get(id=author_id)
        if author == self.request.user:
            return Response({"detail": "Вы не можете подписаться на себя."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user, author=author)
