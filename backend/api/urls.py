from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .recipes_views import IngredientViewSet, TagViewSet, RecipeViewSet
from .users_views import UsersViewSet


app_name = 'api'

router = DefaultRouter()

router.register('users', UsersViewSet, basename='users')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
