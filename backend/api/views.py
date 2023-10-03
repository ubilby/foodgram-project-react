from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from djoser.views import UserViewSet
from rest_framework import generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import AccessToken


from .utils import token_to_email
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import CustomUserSerializer, RecipeSerializer, TagSerializer
from recipes.models import CustomUser, Recipe, Tag


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


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
