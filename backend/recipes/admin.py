from django.contrib import admin

from .models import (
    Ingredient,
    Tag,
    Recipe,
    Favorite,
    Shopping_cart,
    Recipe_ingredients
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
        for ingredient in object.ingredients.all():
            set_ingredient = ', '.join(ingredient.name)
        return set_ingredient

    @admin.display(description='Теги')
    def tags(self, object):
        for tag in object.tags.all():
            set_tag = ', '.join(tag.name)
        return set_tag

    @admin.display(description='В избранном')
    def in_favorites(self, object):
        return object.favorite_recipe.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    list_editable = ('user', 'recipe', )


@admin.register(Shopping_cart)
class Shopping_cartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    list_editable = ('user', 'recipe', )

@admin.register(Recipe_ingredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount', )
    list_editable = ('recipe', 'ingredient', 'amount', )
