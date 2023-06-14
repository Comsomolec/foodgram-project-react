from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import (Ingredient, Tag, Recipe,
                            Recipe_ingredients, Favorite, Shopping_cart)

from .user_serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientsGETSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = Recipe_ingredients
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeIngredientsCREATESerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Recipe_ingredients
        fields = ('id', 'amount', )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'ingredients', 'author',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time', )

    def get_ingredients(self, object):
        ingredients = Recipe_ingredients.objects.filter(recipe=object)
        return RecipeIngredientsGETSerializer(
            ingredients, many=True, read_only=True).data

    def get_is_favorited(self, object):
        return Favorite.objects.filter(
            user=self.context['request'].user, recipe=object).exists()

    def get_is_in_shopping_cart(self, object):
        return Shopping_cart.objects.filter(
            user=self.context['request'].user, recipe=object).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientsCREATESerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'ingredients', 'author', 'name',
                  'image', 'text', 'cooking_time', )

    def validate_ingredients(self, ingredients):
        ingredients_data = []
        for ingredient in ingredients:
            if ingredient.get('id') in ingredients_data:
                raise serializers.ValidationError(
                    'Ингридиенты не должны повторяться'
                )
            ingredients_data.append(ingredient.get('id'))
        return ingredients

    def validate_tags(self, tags):
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                    'Теги не должны повторяться'
                )
        return tags

    @staticmethod
    def recipe_ingredients_create(ingredients, recipe):
        for ingredient in ingredients:
            Recipe_ingredients.objects.bulk_create(
                [Recipe_ingredients(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(pk=ingredient['id']),
                    amount=ingredient['amount']
                )]
            )

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=author, **validated_data)
        recipe.tags.set(tags)
        self.recipe_ingredients_create(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.name)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        instance.tags.clear()
        self.recipe_ingredients_create(
            ingredients=ingredients, recipe=instance)
        instance.tags.set(tags)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeSerializer(instance, context={'request': request}).data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в избранное'
            )
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopping_cart
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Shopping_cart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в список покупок'
            )
        ]


class RecipeCutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )
