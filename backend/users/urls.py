from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import AccountVeiwSet

app_name = 'users'
router = DefaultRouter()
router.register(r'', AccountVeiwSet, basename="user")

urlpatterns = [
    # path('subscriptions/', include(router.urls)),
    # path('<int:pk>/subscribe/', include(router.urls)),
    path('<int:pk>/', include(router.urls)),
    path('', include(router.urls)),
]
