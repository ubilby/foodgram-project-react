from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


from .models import CustomUser
from .serializers import (ChangePasswordSerializer, CustomUserSerializer,
                          CustomUserGetSerializer)
from .permission import IsAuthenticatedOrReadOnlyAndNoDetail


class UserProfileView(RetrieveAPIView):
    serializer_class = CustomUserGetSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user


class UserCreateView(ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny, ]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomUserSerializer
        return CustomUserGetSerializer


class ChangePasswordView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_password = serializer.validated_data.get('current_password')
        if not check_password(current_password, user.password):
            return Response(
                {'detail': 'Wrong password!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        new_password = serializer.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
