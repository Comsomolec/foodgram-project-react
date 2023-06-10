from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import Recipe
from users.models import User, Subscription

FORBIDDEN_NAME = ['me', 'subscriptions', 'subscribe', 'set_password']

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data.get('username') in FORBIDDEN_NAME:
            raise serializers.ValidationError(
                'Данное username использовать запрещено.'
            )
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if User.objects.filter(username=data.get('email')).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

    def update(self, instance, validated_data):
        new_password = validated_data['new_password']
        current_password = validated_data['current_password']
        if not instance.check_password(current_password):
            raise serializers.ValidationError('Неверный пароль')
        if current_password == new_password:
            raise serializers.ValidationError(
                'Пароли не должны совпадать.')
        instance.set_password(new_password)
        instance.save()
        return validated_data

class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, object):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return object.author.filter(user=request.user).exists()

class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author'),
                message='Вы уже подписаны на этого автора'
            ) 
        ]

    def validate(self, data):
        if data['user'] == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.'
            )
        return data

class SubscriptionShowRecipes(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )

class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, object):
        request = self.context.get('request')
        author_recipes = object.recipes.all()
        if request.GET.get('recipes_limit'):
            recipes = recipes[int('recipes_limit')]
        return SubscriptionShowRecipes(author_recipes, many=True).data

    def get_recipes_count(self, object):
        return object.recipes.count()

    def get_is_subscribed(self, object):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return object.author.filter(user=request.user).exists()
