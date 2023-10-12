from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipesViewSet
from favorites.views import FavoriteView
from cart.views import CartView

app_name = 'recipes'
router = DefaultRouter()
router.register(r'', RecipesViewSet)

urlpatterns = [
    path('<int:pk>/favorite/', FavoriteView.as_view(), name='favorite'),
    path('<int:pk>/shopping_cart/', CartView.as_view(), name='cart'),
    path('', include(router.urls)),
]
