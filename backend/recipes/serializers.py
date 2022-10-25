from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from users.serializers import CustomUserSerializer

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class IngredientCreateInRecipeSerializer(serializers.Serializer):
    min_ingredient_amount = 1
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        required=True
    )
    amount = serializers.IntegerField(
        required=True
    )
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )

    def validate_unit(self, value):
        if value < IngredientCreateInRecipeSerializer.min_ingredient_amount:
            raise serializers.ValidationError(
                'Check that the ingredients units is more than one'
            )
        return value

    def get_measurement_unit(self, ingredient):
        return ingredient.ingredient.measurement_unit

    def get_name(self, ingredient):
        return ingredient.ingredient.name


class IngredientInRecipeLiteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = (
            'name',
            'amount'
        )


class RecipeViewSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    author = CustomUserSerializer(
        read_only=True
    )
    ingredients = IngredientInRecipeSerializer(
        many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'image',
            'cooking_time',
            'tags',
            'ingredients',
            'text',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_is_favorited(self, recipe):
        current_user = self.context['request'].user
        if current_user.is_authenticated and Favorite.objects.filter(
                recipe=recipe,
                user=current_user
        ).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, recipe):
        current_user = self.context['request'].user
        if current_user.is_authenticated and ShoppingCart.objects.filter(
                recipe=recipe,
                user=current_user
        ).exists():
            return True
        return False


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = CustomUserSerializer(
        read_only=True
    )
    ingredients = IngredientInRecipeLiteSerializer(
        many=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'image',
            'cooking_time',
            'tags',
            'ingredients',
            'text',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, recipe):
        current_user = self.context['request'].user
        if Favorite.objects.filter(
                recipe=recipe,
                user=current_user
        ).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, recipe):
        current_user = self.context['request'].user
        if ShoppingCart.objects.filter(
                recipe=recipe,
                user=current_user
        ).exists():
            return True
        return False
    @staticmethod
    def __add_ingredients(recipe, ingredients):
        # ingredient_list = []
        # for ingredient in ingredients:
        #     current_ingredient = get_object_or_404(
        #         Ingredient.objects.filter(
        #             id=ingredient['id'])
        #     )
        #     ingredient_list.append(IngredientInRecipe(
        #         ingredient=current_ingredient,
        #         amount=ingredient['amount']))
        #     print(ingredient_list)
        # IngredientInRecipe.objects.bulk_create(ingredient_list)
        # return recipe
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient.objects.filter(
                    id=ingredient['id'])
            )
            ing, _ = IngredientInRecipe.objects.get_or_create(
                ingredient=current_ingredient,
                amount=ingredient['amount'],
            )
            recipe.ingredients.add(ing.id)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        self.__add_ingredients(recipe, ingredients)
        return recipe

    def update(self, recipe, validated_data, ):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            recipe.ingredients.clear()
            self.__add_ingredients(ingredients, recipe)
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            recipe.tags.set(tags_data)
        return super().update(recipe, validated_data)

    def to_representation(self, recipe):
        serializer = RecipeViewSerializer(
            recipe,
            context=self.context
        )
        return serializer.data


class FollowRecipesSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        limit = self.context['request'].query_params.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = obj.recipes.all()[:int(limit)]
        return RecipeViewSerializer(
            recipes,
            many=True
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    ingredient = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('ingredient',)

    def get_ingredient(self, recipe):
        ingredient = recipe.ingredients.all()
        return IngredientSerializer(
            ingredient,
            many=True
        ).data


