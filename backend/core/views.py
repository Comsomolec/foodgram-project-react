from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe
from api.users_serializers import ShowShortRecipes

def favorite_shopping_cart(self, request, pk, model, serializer):
    user = self.request.user
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
    if request.method == 'DELETE':
        get_object_or_404(model, user=user,
                          recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
