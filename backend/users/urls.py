from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import AccountVeiwSet

app_name = 'users'
router = DefaultRouter()
router.register(r'', AccountVeiwSet, basename="user")

urlpatterns = [
    path('<int:pk>/', include(router.urls)),
    path('', include(router.urls)),
]
