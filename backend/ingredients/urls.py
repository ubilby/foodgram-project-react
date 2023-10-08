from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ingredients.views import IngredientsViewSet

app_name = 'ingredients'
router = DefaultRouter()
router.register(r'', IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
