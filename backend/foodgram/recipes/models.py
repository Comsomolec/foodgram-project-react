from django.core.validators import RegexValidator, MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):

    TEST = 'hello'
    name = models.CharField(
        max_length=50,
        verbose_name='Название ингредиента'
        )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'
    

class Tag(models.Model):
    name = models.CharField('Название ингредиента', max_length=50, unique=True)
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет в HEX',
        validators=[
            RegexValidator(
                r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Неверно указана кодировка HEX.'
            )
        ]
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальный идентификатор'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}, {self.slug}'


class Recipe(models.Model):
    
    PATTERN = (
        'Author: {author}, Name: {name}, Date: {date}, Text: {text:.15}.'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Recipe_ingredients',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    image = models.ImageField(upload_to='recipes/', verbose_name='Картинка')
    name = models.CharField(max_length=200, verbose_name='Наименование')
    text = models.TextField(verbose_name='Текст')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        verbose_name='Время приготовления'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.PATTERN.format(
            author=self.author.username,
            group=self.name,
            date=self.pub_date,
            text=self.text,
        )


class Recipe_ingredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='Подписчик'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}' # изменить


class Shopping_cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_user',
        verbose_name='Покупатель'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_recipe',
        verbose_name='Рецепт в корзине'
    )

    class Meta:
        verbose_name = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}' # изменить