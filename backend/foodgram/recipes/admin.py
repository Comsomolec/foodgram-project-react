from django.contrib import admin

from . import models


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit', )
    list_filter = ('name', )
    search_fields = ('name', )


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug', )
    list_editable = ('name', 'color', 'slug', )
    search_fields = ('name', )


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', )
    readonly_fields = ('in_favorites', 'pub_date', )
    list_filter = ('author', 'name', 'tags', )
    empty_value_display = '-None-'
    fileds = (
        'name', 'author', 'text', 'tags', 
        'ingredients', 'cooking_time', 'image', 'pub_date',
    )

    @admin.display(description='Ингредиенты')
    def ingredients(self, object):
        return ', '.join(
            [ingredient.name for ingredient in object.ingredients.all()]
        )

    @admin.display(description='Теги')
    def tags(self, object):
        return ', '.join([tag.name for tag in object.tags.all()])

    @admin.display(description='В избранном')
    def in_favorites(self, obj):
        return obj.favorite_recipe.count()


@admin.register(models.Recipe_ingredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount', )
    list_editable = ('recipe', 'ingredient', 'amount', )


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe', )
    list_editable = ('user', 'recipe', )


@admin.register(models.Shopping_cart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe', )
    list_editable = ('user', 'recipe', )
