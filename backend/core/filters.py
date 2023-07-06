from django_filters.rest_framework import FilterSet
from django_filters.filters import (
    BooleanFilter,
    ModelChoiceField,
    ModelMultipleChoiceFilter
)
from django_filters.widgets import BooleanWidget

from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag
from users.models import User


# class TagFilter(FilterSet):
#   """Фильтрация по тегам."""
#     tags = ModelMultipleChoiceFilter(
#         field_name='tags__slug',
#         to_field_name='slug',
#         queryset=Tag.objects.all()
#         )

#     class Meta:
#         model = Recipe
#         fields = ['tags']


class RecipeFilter(FilterSet):
    """Фильтрация рецептов."""
    author = ModelChoiceField(queryset=User.objects.all())
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorite = BooleanFilter(
        method='filter_is_favorite', widget=BooleanWidget()
    )
    is_in_shopping_cart = BooleanFilter(
        method='filter_is_in_shopping_cart', widget=BooleanWidget()
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorite', 'is_in_shopping_cart']

    def filter_is_favorite(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(recipe_in_cart__user=self.request.user)
        return queryset


class IngredientFilter(SearchFilter):
    """Фильтрация ингредиентов."""
    search_param = 'name'
