from drf_base64.fields import Base64ImageField

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    Recipe_ingredients,
    Favorite,
    Shopping_cart
)
from .users_serializers import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Recipe_ingredients
        fields = ('id', 'amount', )


class RecipeIngredientGetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    class Meta:
        model = Recipe_ingredients
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset = Tag.objects.all(), many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ('author', 'pub_date', )

    def validate_ingredients(self, value):
        ingredients_data = []
        for ingredient in value:
            if ingredient.get('id') in ingredients_data:
                raise serializers.ValidationError(
                    'Ингридиенты не должны повторяться!'
                )
            ingredients_data.append(ingredient.get('id'))
        return value

    def validate_tags(self, value):
        tags_data = []
        for tag in value:
            if tag in tags_data:
                raise serializers.ValidationError(
                    'Теги не должны повторяться!'
                )
            tags_data.append(tag)
        return value

    @staticmethod
    def recipe_ingredient_create(ingredients, recipe):
        for ingredient in ingredients:
            Recipe_ingredients.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            image=validated_data['image'],
            name=validated_data['name'],
            text=validated_data['text'],
            cooking_time=validated_data['cooking_time']
        )
        ingredients = validated_data.pop('ingredients')
        self.recipe_ingredient_create(ingredients, recipe)
        tags = validated_data.pop('tags')
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        self.recipe_ingredient_create(ingredients, instance)
        instance.tags.clear()
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        return super().update(instance, validated_data)


    def to_representation(self, instance):
        return RecipeSerializer(
            instance, context={'request': self.context.get('request')}
        ).data


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
        return RecipeIngredientGetSerializer(
            ingredients, many=True, read_only=True).data

    def get_is_favorited(self, object):
        if self.context['request'].user.is_authenticated:
            return Favorite.objects.filter(
                user=self.context['request'].user, recipe=object).exists()

    def get_is_in_shopping_cart(self, object):
        if self.context['request'].user.is_authenticated:
            return Shopping_cart.objects.filter(
                user=self.context['request'].user, recipe=object).exists()


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
