from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .paginations import CustomPagination
from .permissions import AuthorOrReadOnly
from .recipes_serializers import (
    IngredientSerializer,
    TagSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer
)
from .users_serializers import ShowShortRecipes
from core.filters import RecipeFilter, IngredientFilter
from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    RecipeIngredient,
    Favorite,
    ShoppingCart
)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [IngredientFilter]
    search_fields = ['^name']
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [AuthorOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RecipeFilter
    ordering = ('-pub_date')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeCreateSerializer
        else:
            return RecipeSerializer

    @staticmethod
    def favorite_shopping_cart(request, pk, model, serializer):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = serializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, recipe=recipe)
            content_serializer = ShowShortRecipes(recipe)
            return Response(
                content_serializer.data, status=status.HTTP_201_CREATED
            )
        get_object_or_404(model, user=user,
                          recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated],
        url_path='favorite',
        url_name='favorite',
    )
    def favorite(self, request, pk):
        return self.favorite_shopping_cart(
            request, pk, Favorite, FavoriteSerializer)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated],
        url_path='shopping_cart',
        url_name='shopping_cart',
    )
    def shopping_cart(self, request, pk):
        return self.favorite_shopping_cart(
            request, pk, ShoppingCart, ShoppingCartSerializer
        )

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        ingredient_queryset = RecipeIngredient.objects.filter(
            recipe__recipe_in_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(total=Sum('amount'))
        ingredient_list = [
            f'Список покупок {self.request.user.first_name}\n',
            '|Наименование|  |Ед. изм.|  |Количество|\n'
        ]
        for ingredient in ingredient_queryset:
            ingredient_list.append(
                '|{}|  |{}|  |{}|\n'.format(*ingredient.values())
            )
        response = HttpResponse(ingredient_list, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping cart.txt"'
        )
        return response
