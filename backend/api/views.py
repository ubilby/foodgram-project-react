from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from rest_framework import generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken


from .utils import token_to_email
from .serializers import SignupSerializer, TokenSerializer
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import CustomUserSerializer
from recipes.models import CustomUser


class UserCreateView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny, )
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=["get", "patch"],
        detail=False,
        url_path="me",
        permission_classes=(AllowAny, ),
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == "PATCH":
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.validated_data.pop("role", None)
            serializer.save()
        else:
            serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
