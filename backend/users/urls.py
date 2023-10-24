from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import ChangePasswordView, AccountVeiwSet
from subscribes.views import SubscribeView

app_name = 'users'
router = DefaultRouter()
router.register(r'', AccountVeiwSet, basename="user")

urlpatterns = [
    path('set_password/', ChangePasswordView.as_view(), name='set-password'),
    # path('me/', AccountVeiwSet.as_view(), name='user-profile'),
    path('subscriptions/', SubscribeView.as_view(), name='subscribe'),
    path('<int:pk>/subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('', include(router.urls)),
]
