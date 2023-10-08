from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipesViewSet

app_name = 'recipes'
router = DefaultRouter()
router.register(r'', RecipesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
