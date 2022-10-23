from rest_framework import serializers

from recipes.models import Recipe
from users.models import Follow, User


class FollowingRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionsSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

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
            'recipes_count',
        )

    def get_recipes(self, author):
        recipes = author.recipes.all()[:3]
        return FollowingRecipeSerializer(
            recipes,
            many=True
        ).data

    def get_is_subscribed(self, author):
        current_user = self.context['request'].user.id
        if Follow.objects.filter(
                author=author,
                follower=current_user
        ).exists():
            return True
        return False

    def get_recipes_count(self, author):
        recipes_count = author.recipes.count()
        return recipes_count
