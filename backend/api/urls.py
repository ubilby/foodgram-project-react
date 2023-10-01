from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserCreateView
from recipes.views import RecipeViewSet, TagViewSet


app_name = 'api'
router = DefaultRouter()
router.register(r'users', UserCreateView, basename="user")
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),  # Работа с пользователями
    path('auth/', include('djoser.urls.authtoken')),  # Работа с токенами
]
