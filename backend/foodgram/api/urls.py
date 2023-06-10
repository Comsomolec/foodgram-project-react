from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from .user_views import UsersViewSet
from .views import RecipeViewSet, TagViewSet, IngredientViewSet


app_name = 'api'

router = DefaultRouter()

# router.register('users', UsersViewSet, basename='users')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')
router.register(
    r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
