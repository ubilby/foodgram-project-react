import django_filters
from .models import Recipes


class RecipesFilterSet(django_filters.FilterSet):
    limit = django_filters.NumberFilter(
        method='filter_limit'
    )
    is_favorited = django_filters.NumberFilter(
        field_name='favorites',
        method='filter_is_favorited'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        field_name='cart',
        method='filter_is_in_shopping_cart'
    )
    author = django_filters.NumberFilter(field_name='author__id')
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug', method='filter_tags')

    class Meta:
        model = Recipes
        fields = ['author', 'cart', 'tags']

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == 1 and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == 1 and user.is_authenticated:
            return queryset.filter(cart__user=user)
        return queryset

    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__slug__in=value)

    def filter_limit(self, queryset, name, value):
        return queryset[:value] if value else queryset
