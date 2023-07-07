from django.contrib import admin

from .models import (
    Ingredient,
    Tag,
    Recipe,
    Favorite,
    ShoppingCart,
    RecipeIngredient
)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', )
    list_filter = ('name', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug', )
    list_editable = ('name', 'color', 'slug', )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', )
    readonly_fields = ('in_favorites', )
    list_filter = ('author', 'name', 'tags', )
    fileds = (
        'name', 'author', 'text', 'tags',
        'ingredients', 'cooking_time', 'image', 'pub_date',
    )

    @admin.display(description='Ингредиенты')
    def ingredients(self, object):
        return object.ingredients.value_list('name')

    @admin.display(description='Теги')
    def tags(self, object):
        return object.tags.value_list('name')

    @admin.display(description='В избранном')
    def in_favorites(self, object):
        return object.favorite_recipe.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    list_editable = ('user', 'recipe', )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    list_editable = ('user', 'recipe', )


@admin.register(RecipeIngredient)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount', )
    list_editable = ('recipe', 'ingredient', 'amount', )
