from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import AccountVeiwSet
from subscribes.views import SubscribeView

app_name = 'users'
router = DefaultRouter()
router.register(r'', AccountVeiwSet, basename="user")

urlpatterns = [
    # path('subscriptions/', SubscribeView.as_view(), name='subscribe'),
    # path('<int:pk>/subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('<int:pk>/', include(router.urls)),
    path('', include(router.urls)),
]
