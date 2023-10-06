from users.serializers import ChangePasswordSerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserGetSerializer


class UserProfileView(RetrieveAPIView):
    serializer_class = CustomUserGetSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserCreateView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserCreateView(ModelViewSet):
    queryset = CustomUser.objects.all()

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
