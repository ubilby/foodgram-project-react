from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, TagViewSet
from users.views import UserCreateView, UserProfileView

app_name = 'api'
router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
