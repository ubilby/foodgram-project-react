from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cart.views import CartView, FileView
from favorites.views import FavoriteView

from .views import RecipesViewSet

app_name = 'recipes'
router = DefaultRouter()
router.register(r'', RecipesViewSet)

urlpatterns = [
    # download_shopping_cart/
    path('download_shopping_cart/',
         FileView.as_view(), name='download_file'),
    path('<int:pk>/favorite/', FavoriteView.as_view(), name='favorite'),
    path('<int:pk>/shopping_cart/', CartView.as_view(), name='cart'),
    path('', include(router.urls)),
]
