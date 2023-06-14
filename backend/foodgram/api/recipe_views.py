from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (
    Favorite, Ingredient, Recipe, Recipe_ingredients, Shopping_cart, Tag)
from .filters import RecipeFilter
from .paginations import CustomPagination
from .permissions import AdminAuthorPermission
from .recipe_serializers import (
    IngredientSerializer, RecipeCreateSerializer,
    RecipeSerializer, TagSerializer, RecipeCutSerializer,
    FavoriteSerializer, ShoppingCartSerializer
)
from .utils import create_shopping_cart


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (SearchFilter, )
    search_fields = ('^name', )
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticatedOrReadOnly, AdminAuthorPermission, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(methods=['POST', 'DELETE'],
            detail=True,
            url_path='favorite', )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = FavoriteSerializer(
                data={'user': self.request.user.id, 'recipe': recipe.id})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user, recipe=recipe)
            show_content_serializer = RecipeCutSerializer(recipe)
            return Response(show_content_serializer.data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            get_object_or_404(Favorite, user=request.user,
                              recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST', 'DELETE'],
            detail=True,
            url_path='shopping_cart', )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(
                data={'user': request.user.id, 'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            show_content_serializer = RecipeCutSerializer(recipe)
            return Response(
                show_content_serializer.data, status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            get_object_or_404(
                Shopping_cart, user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        print(Recipe_ingredients.objects.filter(
                recipe__shopping_recipe__user=request.user
            ))
        ingredients_cart = (
            Recipe_ingredients.objects.filter(
                recipe__shopping_recipe__user=request.user
            ).values(
                'ingredient__name',
                'ingredient__measurement_unit',
            ).order_by(
                'ingredient__name'
            ).annotate(ingredient_value=Sum('amount'))
        )
        return create_shopping_cart(ingredients_cart)
