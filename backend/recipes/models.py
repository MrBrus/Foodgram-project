from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=10,
        unique=True,
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Tag color',
        unique=True,
    )
    slug = models.SlugField(
        max_length=10,
        unique=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='ingredient name',
    )
    measurement_unit = models.CharField(
        max_length=10,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='recipe author',
        help_text='Recipe author',
    )
    name = models.CharField(
        max_length=256,
        verbose_name='recipe title',
        db_index=True,
    )
    image = models.ImageField(
        verbose_name='recipe image',
        help_text='Recipe image',
        blank=True,
        null=True,
    )
    cooking_time = models.PositiveSmallIntegerField(
        help_text='Cooking time, min',
        validators=[MinValueValidator(
            1,
            'Cooking time cant be less than 1 min.'
        )],
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        help_text='Please, use exist tags.',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='list of ingredients',
        help_text='Ingredient list',
        through='RecipeIngredient'

    )
    text = models.TextField(
        verbose_name='recipe text',
        help_text='Recipe description',
    )
    pub_date = models.DateTimeField(
        verbose_name='Publication date',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f'{self.name} from {self.author}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Units',
        validators=(
            MinValueValidator(
                0.1,
                message='Minimal ingredients amount is 0,1.'
            ),
        )
    )

    class Meta:
        verbose_name = 'Ingredient amount'
        verbose_name_plural = 'Ingredients amount'

    def __str__(self):
        return f' {self.ingredient} - {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='recipe',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'favorite recipe'
        verbose_name_plural = 'favorited recipes'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe',
                ],
                name='unique favorite recipe for user'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='recipe',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Shopping cart'
        verbose_name_plural = 'Shopping carts'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe',
                ],
                name='unique cart user'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'
