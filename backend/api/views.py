from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from djoser.views import UserViewSet
from rest_framework import generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import AccessToken


from .utils import token_to_email
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import CustomUserSerializer, RecipeSerializer, TagSerializer
from recipes.models import CustomUser, Recipe, Tag


class UserProfileView(RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserCreateView(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
