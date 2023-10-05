from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserCreateView, RecipeViewSet, TagViewSet, UserProfileView


app_name = 'api'
router = DefaultRouter()
router.register(r'users', UserCreateView, basename="user")
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)


urlpatterns = [
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
