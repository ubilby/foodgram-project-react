from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import ChangePasswordView, UserCreateView, UserProfileView

app_name = 'users'
router = DefaultRouter()
router.register(r'', UserCreateView, basename="user")

urlpatterns = [
    path('set_password/', ChangePasswordView.as_view(), name='set-password'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
]
