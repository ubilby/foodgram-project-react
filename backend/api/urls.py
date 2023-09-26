from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet
from .views import get_token, sign_up, UserCreateView


app_name = 'api'
router = DefaultRouter()
# router.register(r'users', UserViewSet, basename="user")

urlpatterns = [
    path('/users/', UserCreateView.as_view(), name='user-create'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),  # Работа с пользователями
    path('', include('djoser.urls.authtoken')),  # Работа с токенами
    # path('auth/signup/', sign_up, name='signup'),
    # path('auth/token/', get_token, name='token'),
]
