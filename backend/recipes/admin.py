from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (
    Favorite, Ingredient, IngredientInRecipe, Recipe, ShoppingCart, Tag
)

EMPTY_VALUE = '-none-'


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    list_editable = (
        'name',
        'color',
        'slug'
    )
    search_fields = (
        'name',
    )
    empty_value_display = EMPTY_VALUE


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_editable = (
        'name',
        'measurement_unit'
    )
    search_fields = (
        'name',
    )
    empty_value_display = EMPTY_VALUE


@admin.register(IngredientInRecipe)
class AdminIngredientInRecipe(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'amount'
    )
    search_fields = (
        'recipe__name',
        'ingredient__name'
    )


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'added_recipes_count',
    )
    search_fields = (
        'author__username',
        'name',
        'tags__name',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    empty_value_display = EMPTY_VALUE

    def added_recipes_count(self, obj):
        return obj.favorite.count()
    added_recipes_count.short_description = ("Count of users, who added "
                                             "recipe in favorited")


admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.unregister(Group)
